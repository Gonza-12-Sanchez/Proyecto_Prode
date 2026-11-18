"""
[API] api/v1/predictions.py - Endpoints de pronósticos (crear, editar, historial).
Ubicación: app/api/v1/predictions.py
Responsabilidad: Capa API - Valida que el partido no haya iniciado, verifica membresía en el torneo y liga,
gestiona concurrencia y expone historial enriquecido.
"""

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user
from database.connection import get_db
from database.models.match import Match
from database.models.prediction import Prediction
from database.models.tournament import Tournament, TournamentParticipant
from database.models.user import User
from app.schemas.prediction import PredictionHistoryEntry, PredictionIn, PredictionOut

router = APIRouter()


@router.post("/matches/{match_id}/predictions", response_model=PredictionOut, status_code=status.HTTP_201_CREATED, summary="Crear pronóstico para un partido")
async def create_prediction(
    match_id: UUID,
    payload: PredictionIn,
    tournament_id: UUID = Query(..., description="ID del torneo en el cual se realiza el pronóstico"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Registra un pronóstico para un partido antes de que comience.
    Valida que el usuario participe en el torneo y que el partido pertenezca a la liga del torneo.
    """
    tournament = await db.scalar(select(Tournament).where(Tournament.id == tournament_id))
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")

    participant = await db.scalar(
        select(TournamentParticipant).where(
            TournamentParticipant.tournament_id == tournament_id,
            TournamentParticipant.user_id == current_user.id,
        )
    )
    if not participant:
        raise HTTPException(status_code=403, detail="You are not a participant in this tournament")

    match = await db.scalar(select(Match).where(Match.id == match_id))
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    if match.league_id != tournament.league_id:
        raise HTTPException(status_code=400, detail="Match does not belong to the tournament league")

    if match.start_time <= datetime.now(timezone.utc):
        raise HTTPException(status_code=409, detail="Match already started")
    if match.status == "FT":
        raise HTTPException(status_code=409, detail="Match already finished")

    existing = await db.scalar(
        select(Prediction).where(
            Prediction.user_id == current_user.id,
            Prediction.tournament_id == tournament_id,
            Prediction.match_id == match_id,
        )
    )
    if existing:
        raise HTTPException(status_code=409, detail="Prediction already exists, use PUT to edit")

    pred = Prediction(
        user_id=current_user.id,
        tournament_id=tournament_id,
        match_id=match_id,
        home_score=payload.home_score,
        away_score=payload.away_score,
    )
    db.add(pred)
    try:
        await db.commit()
        await db.refresh(pred)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Prediction already exists, use PUT to edit")

    return pred


@router.put("/matches/{match_id}/predictions", response_model=PredictionOut, summary="Editar pronóstico existente")
async def update_prediction(
    match_id: UUID,
    payload: PredictionIn,
    tournament_id: UUID = Query(..., description="ID del torneo en el cual se editó el pronóstico"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Permite modificar un pronóstico enviado previamente, siempre y cuando el partido no haya iniciado ni esté finalizado.
    """
    match = await db.scalar(select(Match).where(Match.id == match_id))
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    if match.start_time <= datetime.now(timezone.utc):
        raise HTTPException(status_code=409, detail="Match already started, cannot edit")
    if match.status == "FT":
        raise HTTPException(status_code=409, detail="Predictions locked after result")

    pred = await db.scalar(
        select(Prediction).where(
            Prediction.user_id == current_user.id,
            Prediction.tournament_id == tournament_id,
            Prediction.match_id == match_id,
        )
    )
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction not found")
    if pred.is_scored or pred.points_earned is not None:
        raise HTTPException(status_code=409, detail="Prediction already scored, cannot edit")

    pred.home_score = payload.home_score
    pred.away_score = payload.away_score
    await db.commit()
    await db.refresh(pred)
    return pred


@router.get("/users/me/predictions", response_model=list[PredictionHistoryEntry], summary="Historial de mis pronósticos")
async def list_my_predictions(
    tournament_id: UUID | None = Query(default=None, description="Filtrar por ID de torneo opcional"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retorna el historial completo de pronósticos del usuario con detalles de los equipos,
    resultado real (si ya finalizó) y puntos ganados.
    """
    q = (
        select(Prediction)
        .options(selectinload(Prediction.match))
        .where(Prediction.user_id == current_user.id)
        .order_by(Prediction.created_at.desc())
    )
    if tournament_id:
        q = q.where(Prediction.tournament_id == tournament_id)

    result = await db.scalars(q)
    predictions = result.all()

    history: list[PredictionHistoryEntry] = []
    for p in predictions:
        m = p.match
        history.append(
            PredictionHistoryEntry(
                id=p.id,
                tournament_id=p.tournament_id,
                match_id=p.match_id,
                home_team=m.home_team if m else "Local",
                away_team=m.away_team if m else "Visitante",
                predicted_home=p.home_score,
                predicted_away=p.away_score,
                actual_home=m.home_score if m else None,
                actual_away=m.away_score if m else None,
                points_earned=p.points_earned,
                is_scored=p.is_scored,
                match_status=m.status if m else "UNKNOWN",
                start_time=m.start_time if m else p.created_at,
            )
        )
    return history
