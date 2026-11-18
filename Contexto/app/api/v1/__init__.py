"""
[API] api/v1/__init__.py - Agregador de routers v1.
Ubicación: app/api/v1/__init__.py
Responsabilidad: Capa API - Monta sub-routers auth, tournaments, predictions y matches bajo prefijo /api/v1. Orquesta el cableado sin lógica.
Usa: app.api.v1.auth, app.api.v1.tournaments, app.api.v1.predictions, app.api.v1.matches
No hace: No valida payloads ni consulta DB, solo composición de rutas.
"""

from fastapi import APIRouter

from app.api.v1 import auth, tournaments, predictions, matches, leagues

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(leagues.router, prefix="/leagues", tags=["leagues"])
api_router.include_router(tournaments.router, prefix="/tournaments", tags=["tournaments"])
api_router.include_router(predictions.router, tags=["predictions"])
api_router.include_router(matches.router, tags=["matches"])
