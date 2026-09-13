"""
[DATABASE] connection.py - Conexión PostgreSQL asíncrona y Base declarativa.
Ubicación: database/connection.py
Responsabilidad: Capa DATABASE - Crea el engine async (asyncpg) y Base para todos los modelos. Expone get_db() para inyección en FastAPI.
Usa: app.core.config (settings.DATABASE_URL), sqlalchemy.ext.asyncio
No hace: No define tablas ni lógica de negocio, solo conexión y sesión.
"""

import asyncio
import sys

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Fix Windows ProactorEventLoop incompatibilidad con asyncpg (WinError 64)
# asyncpg requiere SelectorEventLoop en Windows
if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
