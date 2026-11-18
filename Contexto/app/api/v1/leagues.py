"""
[API] api/v1/leagues.py - Endpoint de ligas disponibles.
Ubicación: app/api/v1/leagues.py
Responsabilidad: Capa API - Lista las ligas de fútbol disponibles en la plataforma para creación de torneos o filtros.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from database.models.tournament import League
from app.schemas.tournament import LeagueOut

router = APIRouter()


@router.get("", response_model=list[LeagueOut], summary="Listar ligas disponibles")
async def list_leagues(db: AsyncSession = Depends(get_db)):
    """
    Retorna la lista de ligas disponibles en la plataforma (ej: Premier League, La Liga, etc.)
    con sus identificadores para crear torneos.
    """
    result = await db.scalars(select(League).order_by(League.id))
    return list(result.all())
