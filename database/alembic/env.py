"""
[DATABASE] alembic/env.py - Entorno de migraciones Alembic para PostgreSQL async.
Ubicación: database/alembic/env.py
Responsabilidad: Capa DATABASE - Configura Alembic para autogenerar migraciones desde database.models y ejecutar offline/online contra asyncpg.
Usa: database.connection.Base, database.models, alembic.context
No hace: No define modelos ni ejecuta DDL directo, solo orquesta migraciones.
"""
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Asegurar que la raíz del proyecto (C:/Users/GonziChan/Desktop/Proyecto) esté en sys.path
# para que `import app` y `import database` funcionen cuando alembic se ejecuta desde database/
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import Base y todos los modelos para que target_metadata incluya las 9 tablas
from database.connection import Base  # noqa: E402
import database.models  # noqa: E402,F401

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    import asyncio

    if sys.platform == "win32":
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception:
            pass
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
