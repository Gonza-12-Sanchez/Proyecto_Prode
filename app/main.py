"""
[APP] main.py - Puerta de entrada FastAPI (factory create_app + lifespan).
Ubicación: app/main.py
Responsabilidad: Capa APP - Crea la app FastAPI, registra routers y expone /health y /docs. Lifespan reserva lugar para scheduler APScheduler.
Usa: app.api.v1.api_router
No hace: No conecta a DB directamente ni define modelos, solo ensambla capas.
"""

import asyncio
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router

# Windows fix para asyncpg
if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Scheduler would start here: APScheduler jobs 24h / 10min
    # For scaffold, no-op lifespan
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Prode API",
        version="0.1.0",
        description="Prode MVP - Torneos privados de pronósticos",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/health", tags=["health"])
    async def health():
        return {"status": "ok"}

    return app


app = create_app()
