"""
[DATABASE] models/__init__.py - Índice de todos los modelos SQLAlchemy (9 tablas).
Ubicación: database/models/__init__.py
Responsabilidad: Capa DATABASE - Re-exporta Base y todos los modelos para que Alembic detecte metadata y la app pueda importar desde database.models.
Usa: database.connection.Base, database.models.*
No hace: No define tablas nuevas ni lógica, solo agregación de imports.
"""

from database.connection import Base  # noqa: F401
from database.models.user import User  # noqa: F401
from database.models.tournament import League, ScoringRule, Tournament, TournamentParticipant  # noqa: F401
from database.models.match import Match  # noqa: F401
from database.models.prediction import ChatMessage, Notification, Prediction  # noqa: F401

__all__ = [
    "Base",
    "User",
    "League",
    "Tournament",
    "TournamentParticipant",
    "ScoringRule",
    "Match",
    "Prediction",
    "ChatMessage",
    "Notification",
]
