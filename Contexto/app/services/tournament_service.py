"""
[SERVICES] tournament_service.py - Lógica pura de torneos (estados y códigos).
Ubicación: app/services/tournament_service.py
Responsabilidad: Capa SERVICES - Genera invite_code 8 chars, valida capacidad Free/Premium y transiciones Setup→Active→Completed sin tocar HTTP.
Usa: database.models.tournament.Tournament (solo tipado), sqlalchemy AsyncSession
No hace: No define endpoints ni SQL directo salvo la búsqueda de unicidad de código.
"""

import random
import string

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models.tournament import Tournament

ALPHANUM = string.ascii_uppercase + string.digits


def generate_invite_code(length: int = 8) -> str:
    return "".join(random.choices(ALPHANUM, k=length))


async def generate_unique_invite_code(db: AsyncSession, length: int = 8, max_attempts: int = 10) -> str:
    for _ in range(max_attempts):
        code = generate_invite_code(length)
        exists = await db.scalar(select(Tournament).where(Tournament.invite_code == code))
        if not exists:
            return code
    raise RuntimeError("Failed to generate unique invite_code after attempts")


def can_start_tournament(tournament: Tournament) -> bool:
    return tournament.status == "Setup"


def can_edit_tournament(tournament: Tournament) -> bool:
    return tournament.status == "Setup"


def transition_to_active(tournament: Tournament) -> None:
    if tournament.status != "Setup":
        raise ValueError(f"Cannot start tournament in status {tournament.status}")
    tournament.status = "Active"


def transition_to_completed(tournament: Tournament) -> None:
    if tournament.status != "Active":
        raise ValueError(f"Cannot complete tournament in status {tournament.status}")
    tournament.status = "Completed"


def validate_capacity(is_premium: bool, max_participants: int) -> bool:
    """Free 10 / Premium 50 (MVP); 100 allowed for future compatibility."""
    if is_premium:
        return max_participants in (10, 50, 100)
    return max_participants == 10
