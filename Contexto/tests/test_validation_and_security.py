"""
Tests de seguridad, validación de reglas de negocio y casos de borde.
"""

import uuid
from datetime import datetime, timedelta, timezone
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_validation_and_security_rules(client: AsyncClient):
    uid = uuid.uuid4().hex[:6]
    creator_email = f"creator_{uid}@test.com"
    other_email = f"other_{uid}@test.com"
    pwd = "SecurePassword123!"

    # 1. Validación de longitud de password en registro (<8 chars)
    weak_reg = await client.post("/api/v1/auth/register", json={
        "email": f"weak_{uid}@test.com",
        "username": f"weak_{uid}",
        "password": "123",
    })
    assert weak_reg.status_code == 422

    # Registrar usuarios válidos
    await client.post("/api/v1/auth/register", json={"email": creator_email, "username": f"creator_{uid}", "password": pwd})
    await client.post("/api/v1/auth/register", json={"email": other_email, "username": f"other_{uid}", "password": pwd})

    login_c = await client.post("/api/v1/auth/login", json={"email": creator_email, "password": pwd})
    headers_c = {"Authorization": f"Bearer {login_c.json()['access_token']}"}

    login_o = await client.post("/api/v1/auth/login", json={"email": other_email, "password": pwd})
    headers_o = {"Authorization": f"Bearer {login_o.json()['access_token']}"}

    # 2. Validación de capacidad no permitida (ej: 25 participantes)
    invalid_cap = await client.post("/api/v1/tournaments", headers=headers_c, json={
        "name": "Torneo Inválido",
        "league_id": 39,
        "max_participants": 25,
    })
    assert invalid_cap.status_code == 422

    # Crear torneo válido
    t_resp = await client.post("/api/v1/tournaments", headers=headers_c, json={
        "name": f"Torneo Seguridad {uid}",
        "league_id": 39,
        "max_participants": 10,
    })
    assert t_resp.status_code == 201
    t_id = t_resp.json()["id"]

    # 3. Solo el creador puede iniciar el torneo
    start_other = await client.post(f"/api/v1/tournaments/{t_id}/start", headers=headers_o)
    assert start_other.status_code == 403

    # 4. Usuario no participante no puede consultar partidos del torneo
    matches_other = await client.get(f"/api/v1/tournaments/{t_id}/matches", headers=headers_o)
    assert matches_other.status_code == 403

    # Usuario creador obtiene partidos
    matches_c = await client.get(f"/api/v1/tournaments/{t_id}/matches", headers=headers_c)
    assert matches_c.status_code == 200
    premier_match = matches_c.json()[0]

    # 5. Usuario no participante no puede pronosticar
    pred_non_part = await client.post(
        f"/api/v1/matches/{premier_match['id']}/predictions?tournament_id={t_id}",
        headers=headers_o,
        json={"home_score": 1, "away_score": 0},
    )
    assert pred_non_part.status_code == 403

    # 6. Validación de límite superior de goles (>50)
    huge_score = await client.post(
        f"/api/v1/matches/{premier_match['id']}/predictions?tournament_id={t_id}",
        headers=headers_c,
        json={"home_score": 999, "away_score": 0},
    )
    assert huge_score.status_code == 422

    # 7. Código de invitación inexistente devuelve 404
    bad_code = await client.get("/api/v1/tournaments/preview/ZZZZZZZZ")
    assert bad_code.status_code == 404
