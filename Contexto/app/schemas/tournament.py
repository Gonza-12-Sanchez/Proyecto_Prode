"""
[SCHEMAS] schemas/tournament.py - Validación Pydantic para torneos y leaderboard.
Ubicación: app/schemas/tournament.py
Responsabilidad: Capa SCHEMAS - Define TournamentCreate (name 1-120, league_id, max_participants), ScoringRules y vistas TournamentOut/Preview/Leaderboard.
Usa: pydantic
No hace: No genera códigos ni toca DB, solo valida payloads HTTP.
"""

from datetime import datetime
from uuid import UUID

from typing import Literal

from pydantic import BaseModel, Field


class LeagueOut(BaseModel):
    id: int
    name: str
    country: str | None = None
    logo_url: str | None = None

    model_config = {"from_attributes": True}


class ScoringRulesIn(BaseModel):
    exact_score: int = Field(default=5, ge=0)
    correct_winner: int = Field(default=3, ge=0)
    goal_difference: int = Field(default=2, ge=0)


class ScoringRulesOut(ScoringRulesIn):
    pass


class TournamentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None
    league_id: int
    max_participants: Literal[10, 50, 100] = Field(
        default=10,
        description="Capacidad máxima de participantes (10 para Free; 50 o 100 para Premium)"
    )
    scoring_rules: ScoringRulesIn | None = None


class TournamentOut(BaseModel):
    id: UUID
    name: str
    description: str | None
    league_id: int
    creator_id: UUID
    invite_code: str
    max_participants: int
    status: str
    created_at: datetime
    scoring_rules: ScoringRulesOut | None = None

    model_config = {"from_attributes": True}


class JoinByCodeIn(BaseModel):
    invite_code: str = Field(min_length=8, max_length=8, pattern=r"^[A-Za-z0-9]{8}$")


class TournamentPreviewOut(BaseModel):
    id: UUID
    name: str
    league_id: int
    league_name: str | None = None
    max_participants: int
    current_participants: int
    scoring_rules: ScoringRulesOut | None = None
    status: str


class LeaderboardEntry(BaseModel):
    user_id: UUID
    username: str
    total_points: int
    predictions_count: int
    accuracy: float
    rank: int


class LeaderboardOut(BaseModel):
    tournament_id: UUID
    entries: list[LeaderboardEntry]
    my_rank: int | None = None
    my_points: int | None = None
