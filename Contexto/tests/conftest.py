"""
Configuración de fixtures globales para pytest.
"""

import asyncio
import sys
import pytest
from httpx import ASGITransport, AsyncClient

# Asegurar Windows SelectorEventLoop en Windows para asyncpg / psycopg
if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

from app.main import app


@pytest.fixture(scope="session")
def event_loop():
    """Crea un event loop de sesión con la política adecuada."""
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    """Cliente HTTP asíncrono para interactuar con los endpoints de FastAPI."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
