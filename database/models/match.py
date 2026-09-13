"""
[DATABASE] models/match.py - Modelo Match (tabla matches).
Ubicación: database/models/match.py
Responsabilidad: Capa DATABASE - Define la tabla matches ligada a leagues, con fixtures y resultados. Soporta ventana 7 días y status NS/LIVE/FT.
Usa: database.connection.Base
No hace: No sincroniza con Football API, solo persiste partidos ya normalizados.
"""

import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, BigInteger, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connection import Base


class Match(Base):
    __tablename__ = "matches"
    __table_args__ = (
        CheckConstraint("status IN ('NS','LIVE','FT','POSTPONED','CANCELLED')", name="ck_matches_status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    api_id: Mapped[int | None] = mapped_column(BigInteger, unique=True, nullable=True)  # external_id
    league_id: Mapped[int] = mapped_column(Integer, ForeignKey("leagues.id"), nullable=False, index=True)
    home_team: Mapped[str] = mapped_column(String(80), nullable=False)
    away_team: Mapped[str] = mapped_column(String(80), nullable=False)
    venue: Mapped[str | None] = mapped_column(String(120), nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="NS")
    home_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    away_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    league: Mapped["League"] = relationship("League", back_populates="matches", lazy="joined")  # type: ignore
    predictions: Mapped[list["Prediction"]] = relationship("Prediction", back_populates="match", lazy="selectin")  # type: ignore
