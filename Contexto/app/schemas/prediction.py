"""
[SCHEMAS] schemas/prediction.py - Validación Pydantic para predicciones y partidos.
Ubicación: app/schemas/prediction.py
Responsabilidad: Capa SCHEMAS - Define PredictionIn (home/away >=0), PredictionOut y MatchOut para serializar matches 7 días y predicciones.
Usa: pydantic
No hace: No valida bloqueo temporal ni scoring, solo tipos y rangos.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class PredictionIn(BaseModel):
    home_score: int = Field(ge=0, le=50, description="Goles del equipo local (0 a 50)")
    away_score: int = Field(ge=0, le=50, description="Goles del equipo visitante (0 a 50)")


class PredictionOut(BaseModel):
    id: UUID
    user_id: UUID
    tournament_id: UUID
    match_id: UUID
    home_score: int
    away_score: int
    points_earned: int | None
    is_scored: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class MatchResultIn(BaseModel):
    home_score: int = Field(ge=0, le=50, description="Goles reales del equipo local")
    away_score: int = Field(ge=0, le=50, description="Goles reales del equipo visitante")


class PredictionHistoryEntry(BaseModel):
    id: UUID
    tournament_id: UUID
    match_id: UUID
    home_team: str
    away_team: str
    predicted_home: int
    predicted_away: int
    actual_home: int | None
    actual_away: int | None
    points_earned: int | None
    is_scored: bool
    match_status: str
    start_time: datetime


class MatchOut(BaseModel):
    id: UUID
    league_id: int
    home_team: str
    away_team: str
    venue: str | None
    start_time: datetime
    status: str
    home_score: int | None
    away_score: int | None
    my_prediction: PredictionOut | None = None

    model_config = {"from_attributes": True}
