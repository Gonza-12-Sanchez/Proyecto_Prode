"""
[API] api/v1/matches.py - Endpoints de partidos por torneo y liquidación de resultados.
Ubicación: app/api/v1/matches.py
Responsabilidad: Capa API - Lista partidos disponibles en la ventana de días solicitada y permite simular/cargar resultados oficiales.
"""

from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from database.connection import get_db
from database.models.match import Match
from database.models.prediction import Prediction
from database.models.tournament import Tournament, TournamentParticipant
from database.models.user import User
from app.schemas.prediction import MatchOut, MatchResultIn, PredictionOut
from app.services.scoring_service import settle_match_scoring

router = APIRouter()


@router.get("/tournaments/{tournament_id}/matches", response_model=list[MatchOut], summary="Listar partidos de un torneo")
async def list_matches(
    tournament_id: UUID,
    next_days: int = Query(default=7, ge=1, le=30, description="Días hacia adelante a consultar (1 a 30)"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retorna los partidos programados para la liga del torneo dentro de la ventana de días especificada.
    Incluye si el usuario autenticado ya realizó un pronóstico para cada partido.
    """
    tournament = await db.scalar(select(Tournament).where(Tournament.id == tournament_id))
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    # Verificar si el usuario participa en el torneo
    participant = await db.scalar(
        select(TournamentParticipant).where(
            TournamentParticipant.tournament_id == tournament_id,
            TournamentParticipant.user_id == current_user.id,
        )
    )
    if not participant:
        raise HTTPException(status_code=403, detail="Must be a participant of the tournament to view matches")

    now = datetime.now(timezone.utc)
    until = now + timedelta(days=next_days)
    q = (
        select(Match)
        .where(Match.league_id == tournament.league_id)
        .where(Match.start_time >= now)
        .where(Match.start_time <= until)
        .order_by(Match.start_time.asc())
    )
    result = await db.scalars(q)
    matches = result.all()

    # Obtener las predicciones del usuario para estos partidos en este torneo
    match_ids = [m.id for m in matches]
    user_preds_res = await db.scalars(
        select(Prediction).where(
            Prediction.user_id == current_user.id,
            Prediction.tournament_id == tournament_id,
            Prediction.match_id.in_(match_ids),
        )
    )
    user_preds = {p.match_id: p for p in user_preds_res.all()}

    out: list[MatchOut] = []
    for m in matches:
        pred = user_preds.get(m.id)
        pred_out = PredictionOut.model_validate(pred) if pred else None
        out.append(
            MatchOut(
                id=m.id,
                league_id=m.league_id,
                home_team=m.home_team,
                away_team=m.away_team,
                venue=m.venue,
                start_time=m.start_time,
                status=m.status,
                home_score=m.home_score,
                away_score=m.away_score,
                my_prediction=pred_out,
            )
        )
    return out


@router.post("/matches/{match_id}/result", summary="Finalizar partido y liquidar puntuaciones (Testing/Swagger)")
async def finalize_match_result(
    match_id: UUID,
    payload: MatchResultIn,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Simula o registra el resultado final de un partido de fútbol (`status='FT'`).
    Calcula automáticamente los puntos para todos los pronósticos asociados,
    actualiza los totales de los participantes y refresca la tabla de posiciones.
    """
    match = await db.scalar(select(Match).where(Match.id == match_id))
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    res = await settle_match_scoring(
        db=db,
        match_id=match_id,
        home_score=payload.home_score,
        away_score=payload.away_score,
    )
    return {
        "message": f"Partido {match.home_team} vs {match.away_team} finalizado con éxito",
        "result": f"{payload.home_score} - {payload.away_score}",
        "details": res,
    }
