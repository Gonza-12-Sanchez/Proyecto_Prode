"""
[WORKERS] football_sync.py - Adapter Football API + workers 24h/10min (cadete).
Ubicación: app/workers/football_sync.py
Responsabilidad: Capa WORKERS - Implementa patrón Adapter (ApiFootballAdapter vs MockAdapter), factory get_adapter() según MOCK_MODE y jobs sync_fixtures/sync_results con retry 3×/5s y timeout 30s.
Usa: app.core.config.settings, httpx, app.mocks/*.json
No hace: No define endpoints ni modelos SQL, solo orquesta I/O externa y normaliza datos para que services los persistan.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Protocol

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class MatchDTO(dict):
    pass


class ResultDTO(dict):
    pass


class FootballPort(Protocol):
    async def get_fixtures(self, league_id: int, next_days: int = 7) -> list[dict]: ...

    async def get_results(self, match_ids: list[int]) -> list[dict]: ...


class ApiFootballAdapter:
    """Real Football API via httpx - timeout 30s, retry 3x /5s."""

    BASE = settings.FOOTBALL_API_BASE

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.FOOTBALL_API_KEY
        self.timeout = 30
        self.max_retries = 3
        self.retry_delay = 5

    async def _get(self, path: str, params: dict | None = None) -> dict:
        headers = {"x-apisports-key": self.api_key} if self.api_key else {}
        url = f"{self.BASE}{path}"
        last_exc: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    resp = await client.get(url, params=params, headers=headers)
                    resp.raise_for_status()
                    return resp.json()
            except (httpx.TimeoutException, httpx.HTTPStatusError, httpx.RequestError) as exc:
                last_exc = exc
                logger.warning("ApiFootballAdapter _get attempt %s/%s failed: %s", attempt, self.max_retries, exc)
                if attempt < self.max_retries:
                    await asyncio.sleep(self.retry_delay)
        logger.error("ApiFootballAdapter failed after %s attempts for %s", self.max_retries, path)
        raise last_exc  # type: ignore

    async def get_fixtures(self, league_id: int, next_days: int = 7) -> list[dict]:
        # Example mapping to API-Football v3; implement pagination as needed
        data = await self._get("/fixtures", params={"league": league_id, "next": next_days})
        # Normalize response["response"] -> list[dict]
        if isinstance(data, dict) and "response" in data:
            return data["response"]
        return data if isinstance(data, list) else []  # type: ignore

    async def get_results(self, match_ids: list[int]) -> list[dict]:
        # Poll live/finished; API-Football uses ids param
        params = {"ids": "-".join(map(str, match_ids))} if match_ids else {}
        data = await self._get("/fixtures", params=params)
        if isinstance(data, dict) and "response" in data:
            return data["response"]
        return data if isinstance(data, list) else []  # type: ignore


class MockAdapter:
    """Fallback determinístico: lee app/mocks/*.json."""

    def __init__(self, mocks_dir: Path | None = None):
        self.mocks_dir = mocks_dir or Path(__file__).parent.parent / "mocks"

    def _load(self, filename: str) -> list[dict]:
        p = self.mocks_dir / filename
        if not p.exists():
            logger.warning("Mock file not found: %s", p)
            return []
        return json.loads(p.read_text(encoding="utf-8"))

    async def get_fixtures(self, league_id: int, next_days: int = 7) -> list[dict]:
        # fixtures.json contains fixtures for all leagues; filter by league_id
        fixtures = self._load("fixtures.json")
        if not fixtures:
            return []
        # if fixtures have league_id field, filter; else return all
        filtered = [f for f in fixtures if f.get("league_id") == league_id or f.get("league", {}).get("id") == league_id]
        return filtered if filtered else fixtures

    async def get_results(self, match_ids: list[int]) -> list[dict]:
        results = self._load("results.json")
        if not results:
            return []
        if match_ids:
            # filter by api_id or id
            wanted = set(match_ids)
            return [r for r in results if r.get("api_id") in wanted or r.get("id") in wanted]
        return results


def get_adapter() -> FootballPort:
    """Factory según MOCK_MODE."""
    if settings.MOCK_MODE or not settings.FOOTBALL_API_KEY:
        logger.info("Using MockAdapter (MOCK_MODE=%s)", settings.MOCK_MODE)
        return MockAdapter()
    logger.info("Using ApiFootballAdapter")
    return ApiFootballAdapter()  # type: ignore


async def sync_fixtures(db=None) -> dict:
    """Job 24h: pull fixtures por liga, upsert excluyendo incompletos sin team/date/time."""
    adapter = get_adapter()
    leagues = [39, 140, 135, 78, 61]  # Premier, La Liga, Serie A, Bundesliga, Ligue 1 (api ids)
    total = 0
    fallback_used = isinstance(adapter, MockAdapter)
    for league_id in leagues:
        try:
            fixtures = await adapter.get_fixtures(league_id, next_days=7)
        except Exception as exc:
            logger.error("sync_fixtures league %s failed: %s", league_id, exc)
            # fallback to mock if real adapter fails
            if not isinstance(adapter, MockAdapter):
                logger.info("Falling back to MockAdapter for league %s", league_id)
                fallback_used = True
                fixtures = await MockAdapter().get_fixtures(league_id)
            else:
                continue
        # Filter incomplete: require team/date/time
        valid = []
        for f in fixtures:
            # Support both flat and nested API shapes
            home = f.get("home_team") or f.get("teams", {}).get("home", {}).get("name")
            away = f.get("away_team") or f.get("teams", {}).get("away", {}).get("name")
            start = f.get("start_time") or f.get("fixture", {}).get("date")
            if not home or not away or not start:
                logger.debug("Skipping incomplete fixture: %s", f)
                continue
            valid.append(f)
        logger.info("sync_fixtures league=%s fetched=%s valid=%s fallback_used=%s", league_id, len(fixtures), len(valid), fallback_used)
        total += len(valid)
        # TODO: upsert into DB (matches table) when db provided
        # async with db: await upsert_matches(valid)
    return {"synced": total, "fallback_used": fallback_used}


async def sync_results(db=None) -> dict:
    """Polling 10min: retrieve final scores, update <1min, trigger scoring."""
    adapter = get_adapter()
    fallback_used = isinstance(adapter, MockAdapter)
    try:
        results = await adapter.get_results([])
    except Exception as exc:
        logger.error("sync_results failed: %s", exc)
        if not isinstance(adapter, MockAdapter):
            logger.info("Falling back to MockAdapter for results")
            fallback_used = True
            results = await MockAdapter().get_results([])
        else:
            return {"updated": 0, "fallback_used": fallback_used, "error": str(exc)}
    valid = [r for r in results if r.get("home_score") is not None and r.get("away_score") is not None]
    logger.info("sync_results fetched=%s valid=%s fallback_used=%s", len(results), len(valid), fallback_used)
    # TODO: update matches set status=FT and trigger scoring_service.score_match
    return {"updated": len(valid), "fallback_used": fallback_used}
