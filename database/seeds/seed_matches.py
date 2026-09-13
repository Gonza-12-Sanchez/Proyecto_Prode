"""
[DATABASE] seeds/seed_matches.py - Carga partidos futuros de prueba para Premier League y La Liga.
"""
import asyncio
import sys
import uuid
from datetime import datetime, timedelta, timezone

sys.path.insert(0, r"c:\Users\GonziChan\Desktop\Proyecto")

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


async def seed_matches():
    engine = create_async_engine(settings.DATABASE_URL)
    now = datetime.now(timezone.utc)

    # 5 partidos Premier League (39), 5 partidos La Liga (140) en los próximos 1 a 6 días
    sample_fixtures = [
        # Premier League (39)
        (uuid.uuid4(), 9001, 39, "Arsenal", "Manchester City", "Emirates Stadium", now + timedelta(days=1), "NS"),
        (uuid.uuid4(), 9002, 39, "Liverpool", "Chelsea", "Anfield", now + timedelta(days=1, hours=4), "NS"),
        (uuid.uuid4(), 9003, 39, "Manchester United", "Tottenham", "Old Trafford", now + timedelta(days=2), "NS"),
        (uuid.uuid4(), 9004, 39, "Aston Villa", "Newcastle", "Villa Park", now + timedelta(days=3), "NS"),
        (uuid.uuid4(), 9005, 39, "Brighton", "West Ham", "Amex Stadium", now + timedelta(days=4), "NS"),
        # La Liga (140)
        (uuid.uuid4(), 9101, 140, "Real Madrid", "Barcelona", "Santiago Bernabeu", now + timedelta(days=1), "NS"),
        (uuid.uuid4(), 9102, 140, "Atletico Madrid", "Sevilla", "Metropolitano", now + timedelta(days=2), "NS"),
        (uuid.uuid4(), 9103, 140, "Real Betis", "Villarreal", "Benito Villamarin", now + timedelta(days=2, hours=3), "NS"),
        (uuid.uuid4(), 9104, 140, "Athletic Club", "Real Sociedad", "San Mames", now + timedelta(days=3), "NS"),
        (uuid.uuid4(), 9105, 140, "Valencia", "Celta de Vigo", "Mestalla", now + timedelta(days=5), "NS"),
    ]

    async with engine.begin() as conn:
        for f in sample_fixtures:
            await conn.execute(
                text("""
                INSERT INTO matches (id, api_id, league_id, home_team, away_team, venue, start_time, status)
                VALUES (:id, :api_id, :league_id, :home_team, :away_team, :venue, :start_time, :status)
                ON CONFLICT (api_id) DO UPDATE SET
                    start_time = EXCLUDED.start_time,
                    status = EXCLUDED.status;
                """),
                {
                    "id": f[0],
                    "api_id": f[1],
                    "league_id": f[2],
                    "home_team": f[3],
                    "away_team": f[4],
                    "venue": f[5],
                    "start_time": f[6],
                    "status": f[7],
                }
            )
        print(f"Partidos sembrados exitosamente: {len(sample_fixtures)} fixtures en base de datos.")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_matches())
