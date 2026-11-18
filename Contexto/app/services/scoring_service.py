"""
[SERVICES] scoring_service.py - Orquestación de liquidación de partidos y cálculo de puntuaciones.
Ubicación: app/services/scoring_service.py
Responsabilidad: Capa SERVICES - Cierra partidos a FT, liquida predicciones con calculate_points(),
actualiza tournament_participants (puntos, precisión, ranking) y rachas de usuarios.
"""

from decimal import Decimal
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.models.match import Match
from database.models.prediction import Prediction
from database.models.tournament import ScoringRule, TournamentParticipant
from database.models.user import User
from app.services.scoring import calculate_points, ScoringRules


async def settle_match_scoring(
    db: AsyncSession,
    match_id: UUID,
    home_score: int,
    away_score: int,
) -> dict:
    """
    Finaliza un partido con su resultado oficial y liquida todas las predicciones asociadas.
    Actualiza puntos, rachas y tablas de posiciones en una sola transacción atómica.
    """
    # 1. Obtener y actualizar el partido
    match = await db.scalar(select(Match).where(Match.id == match_id))
    if not match:
        raise ValueError(f"Match {match_id} not found")

    match.home_score = home_score
    match.away_score = away_score
    match.status = "FT"

    # 2. Buscar todas las predicciones no puntuadas para este partido
    q_preds = (
        select(Prediction)
        .where(Prediction.match_id == match_id, Prediction.is_scored == False)
    )
    preds_result = await db.scalars(q_preds)
    predictions = preds_result.all()

    if not predictions:
        await db.commit()
        return {"match_id": match_id, "status": "FT", "scored_predictions": 0}

    # 3. Cargar reglas de puntuación de los torneos involucrados
    tournament_ids = {p.tournament_id for p in predictions}
    rules_result = await db.scalars(
        select(ScoringRule).where(ScoringRule.tournament_id.in_(tournament_ids))
    )
    tournament_rules: dict[UUID, ScoringRules] = {
        r.tournament_id: ScoringRules(
            exact=r.exact_score,
            winner=r.correct_winner,
            difference=r.goal_difference,
        )
        for r in rules_result.all()
    }

    # 4. Calcular puntos para cada predicción
    user_points_map: dict[tuple[UUID, UUID], int] = {}  # (tournament_id, user_id) -> points
    user_streak_updates: dict[UUID, bool] = {}  # user_id -> was_correct

    for p in predictions:
        rules = tournament_rules.get(p.tournament_id, ScoringRules())
        pts = calculate_points(
            pred_home=p.home_score,
            pred_away=p.away_score,
            actual_home=home_score,
            actual_away=away_score,
            rules=rules,
        )
        p.points_earned = pts
        p.is_scored = True

        user_points_map[(p.tournament_id, p.user_id)] = pts
        # Un pronóstico es acertado si sumó al menos 1 punto
        user_streak_updates[p.user_id] = pts > 0

    # 5. Actualizar tournament_participants
    for (t_id, u_id), pts in user_points_map.items():
        participant = await db.scalar(
            select(TournamentParticipant).where(
                TournamentParticipant.tournament_id == t_id,
                TournamentParticipant.user_id == u_id,
            )
        )
        if participant:
            participant.total_points += pts
            participant.predictions_count += 1

            # Calcular porcentaje de acierto del participante en este torneo
            scored_preds = await db.scalars(
                select(Prediction).where(
                    Prediction.tournament_id == t_id,
                    Prediction.user_id == u_id,
                    Prediction.is_scored == True,
                )
            )
            all_user_preds = scored_preds.all()
            correct_count = sum(1 for pr in all_user_preds if (pr.points_earned or 0) > 0)
            total_count = len(all_user_preds)
            if total_count > 0:
                participant.accuracy = Decimal(str(round((correct_count / total_count) * 100, 2)))

    # 6. Actualizar rachas de usuarios
    for u_id, was_correct in user_streak_updates.items():
        user = await db.scalar(select(User).where(User.id == u_id))
        if user:
            if was_correct:
                user.current_streak += 1
                if user.current_streak > user.longest_streak:
                    user.longest_streak = user.current_streak
            else:
                user.current_streak = 0

    # 7. Recalcular rankings en los torneos involucrados
    for t_id in tournament_ids:
        parts_res = await db.scalars(
            select(TournamentParticipant)
            .where(TournamentParticipant.tournament_id == t_id)
            .order_by(
                TournamentParticipant.total_points.desc(),
                TournamentParticipant.accuracy.desc(),
                TournamentParticipant.joined_at.asc(),
            )
        )
        for rank_idx, part in enumerate(parts_res.all(), start=1):
            part.rank = rank_idx

    await db.commit()
    return {
        "match_id": match_id,
        "status": "FT",
        "scored_predictions": len(predictions),
        "tournaments_updated": len(tournament_ids),
    }
