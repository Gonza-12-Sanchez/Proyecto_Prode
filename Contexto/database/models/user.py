"""
[DATABASE] models/user.py - Modelo User (tabla users).
Ubicación: database/models/user.py
Responsabilidad: Capa DATABASE - Define la tabla users con validaciones de email/username, rachas y premium. Es la entidad central de autenticación.
Usa: database.connection.Base, sqlalchemy.orm
No hace: No hashea passwords ni genera JWT, solo persistencia.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.connection import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    # favorite_teams stored as comma-separated or JSON; MVP: Text array via string or JSONB placeholder
    # Using Text for simplicity without PG array in SQLite compat; for Postgres array use ARRAY(Text)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    premium_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    current_streak: Mapped[int] = mapped_column(default=0, nullable=False)
    longest_streak: Mapped[int] = mapped_column(default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    tournaments_created: Mapped[list["Tournament"]] = relationship("Tournament", back_populates="creator", lazy="select")  # type: ignore
    participations: Mapped[list["TournamentParticipant"]] = relationship("TournamentParticipant", back_populates="user", lazy="select")  # type: ignore
    predictions: Mapped[list["Prediction"]] = relationship("Prediction", back_populates="user", lazy="select")  # type: ignore
