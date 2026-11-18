"""
[DATABASE] models/tournament.py - Modelos League, Tournament, TournamentParticipant y ScoringRule.
Ubicación: database/models/tournament.py
Responsabilidad: Capa DATABASE - Define tablas leagues, tournaments, tournament_participants y scoring_rules con CHECK, UNIQUE y FKs. Modela el dominio de torneos privados.
Usa: database.connection.Base
No hace: No genera invite_code ni valida capacidad premium, eso es lógica de services.
"""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text, func, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connection import Base


class League(Base):
    __tablename__ = "leagues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # e.g. 39 Premier
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    country: Mapped[str | None] = mapped_column(String(80), nullable=True)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    api_id: Mapped[int | None] = mapped_column(Integer, unique=True, nullable=True)  # external_id

    tournaments: Mapped[list["Tournament"]] = relationship("Tournament", back_populates="league", lazy="selectin")  # type: ignore
    matches: Mapped[list["Match"]] = relationship("Match", back_populates="league", lazy="selectin")  # type: ignore


class Tournament(Base):
    __tablename__ = "tournaments"
    __table_args__ = (
        CheckConstraint("max_participants IN (10, 50, 100)", name="ck_tournaments_max_participants"),
        CheckConstraint("status IN ('Setup','Active','Completed')", name="ck_tournaments_status"),
        CheckConstraint("invite_code ~ '^[A-Za-z0-9]{8}$'", name="ck_tournaments_invite_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    league_id: Mapped[int] = mapped_column(Integer, ForeignKey("leagues.id"), nullable=False, index=True)
    creator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    invite_code: Mapped[str] = mapped_column(String(8), unique=True, nullable=False, index=True)
    max_participants: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    status: Mapped[str] = mapped_column(String(10), nullable=False, default="Setup")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    league: Mapped["League"] = relationship("League", back_populates="tournaments", lazy="joined")  # type: ignore
    creator: Mapped["User"] = relationship("User", back_populates="tournaments_created", lazy="joined")  # type: ignore
    participants: Mapped[list["TournamentParticipant"]] = relationship("TournamentParticipant", back_populates="tournament", cascade="all, delete-orphan", lazy="selectin")  # type: ignore
    scoring_rule: Mapped["ScoringRule"] = relationship("ScoringRule", back_populates="tournament", uselist=False, cascade="all, delete-orphan", lazy="joined")  # type: ignore


class TournamentParticipant(Base):
    __tablename__ = "tournament_participants"

    tournament_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tournaments.id", ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    total_points: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    predictions_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    accuracy: Mapped[float] = mapped_column(Numeric(5, 2), default=0, nullable=False)
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)

    tournament: Mapped["Tournament"] = relationship("Tournament", back_populates="participants", lazy="joined")  # type: ignore
    user: Mapped["User"] = relationship("User", back_populates="participations", lazy="joined")  # type: ignore


class ScoringRule(Base):
    __tablename__ = "scoring_rules"
    __table_args__ = (
        CheckConstraint("exact_score >= 0", name="ck_scoring_exact"),
        CheckConstraint("correct_winner >= 0", name="ck_scoring_winner"),
        CheckConstraint("goal_difference >= 0", name="ck_scoring_diff"),
    )

    tournament_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("tournaments.id", ondelete="CASCADE"), primary_key=True)
    exact_score: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    correct_winner: Mapped[int] = mapped_column(Integer, nullable=False, default=3)
    goal_difference: Mapped[int] = mapped_column(Integer, nullable=False, default=2)

    tournament: Mapped["Tournament"] = relationship("Tournament", back_populates="scoring_rule", lazy="joined")  # type: ignore
