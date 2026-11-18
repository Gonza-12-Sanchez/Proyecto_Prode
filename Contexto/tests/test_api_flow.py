"""
Test de integración end-to-end del flujo completo de Prode MVP:
1. Registro y Login de 2 usuarios
2. Creación de torneo por Usuario A
3. Previsualización y Join por Usuario B
4. Consulta de partidos de la liga
5. Envío de pronósticos antes del partido
6. Finalización y liquidación del resultado del partido
7. Verificación de la tabla de posiciones (Leaderboard) y estadísticas de perfil
"""

import uuid
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_full_prode_mvp_flow(client: AsyncClient):
    uid = uuid.uuid4().hex[:6]
    user_a_email = f"usera_{uid}@test.com"
    user_a_name = f"usera_{uid}"
    user_b_email = f"userb_{uid}@test.com"
    user_b_name = f"userb_{uid}"
    pwd = "Password123!"

    # 1. Registro Usuario A y B
    resp_a = await client.post("/api/v1/auth/register", json={
        "email": user_a_email,
        "username": user_a_name,
        "password": pwd,
    })
    assert resp_a.status_code == 201, resp_a.text

    resp_b = await client.post("/api/v1/auth/register", json={
        "email": user_b_email,
        "username": user_b_name,
        "password": pwd,
    })
    assert resp_b.status_code == 201, resp_b.text

    # 2. Login Usuario A y B
    login_a = await client.post("/api/v1/auth/login", json={"email": user_a_email, "password": pwd})
    assert login_a.status_code == 200
    token_a = login_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    login_b = await client.post("/api/v1/auth/login", json={"email": user_b_email, "password": pwd})
    assert login_b.status_code == 200
    token_b = login_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # 3. Listar Ligas disponibles
    leagues_resp = await client.get("/api/v1/leagues")
    assert leagues_resp.status_code == 200
    leagues = leagues_resp.json()
    assert len(leagues) >= 1
    league_39 = next((l for l in leagues if l["id"] == 39), leagues[0])
    league_id = league_39["id"]

    # 4. Usuario A crea un torneo
    t_resp = await client.post(
        "/api/v1/tournaments",
        headers=headers_a,
        json={
            "name": f"Torneo Amigos {uid}",
            "description": "El mejor torneo de predicciones",
            "league_id": league_id,
            "max_participants": 10,
            "scoring_rules": {
                "exact_score": 5,
                "correct_winner": 3,
                "goal_difference": 2,
            },
        },
    )
    assert t_resp.status_code == 201, t_resp.text
    tournament = t_resp.json()
    tournament_id = tournament["id"]
    invite_code = tournament["invite_code"]
    assert len(invite_code) == 8

    # 5. Usuario B previsualiza el torneo por código
    preview_resp = await client.get(f"/api/v1/tournaments/preview/{invite_code}")
    assert preview_resp.status_code == 200, preview_resp.text
    preview_data = preview_resp.json()
    assert preview_data["name"] == tournament["name"]
    assert preview_data["current_participants"] == 1

    # 6. Usuario B se une al torneo con el código
    join_resp = await client.post(
        "/api/v1/tournaments/join",
        headers=headers_b,
        json={"invite_code": invite_code},
    )
    assert join_resp.status_code == 200, join_resp.text
    assert join_resp.json()["current_participants"] == 2

    # Intentar unirse nuevamente debe dar 409 Conflict
    join_duplicate = await client.post(
        "/api/v1/tournaments/join",
        headers=headers_b,
        json={"invite_code": invite_code},
    )
    assert join_duplicate.status_code == 409

    # 7. Usuario A inicia el torneo
    start_resp = await client.post(f"/api/v1/tournaments/{tournament_id}/start", headers=headers_a)
    assert start_resp.status_code == 200
    assert start_resp.json()["status"] == "Active"

    # 8. Insertar un partido fresco específico para esta ejecución
    from datetime import datetime, timedelta, timezone
    from database.connection import AsyncSessionLocal
    from database.models.match import Match

    fresh_match_id = uuid.uuid4()
    async with AsyncSessionLocal() as session:
        fresh_match = Match(
            id=fresh_match_id,
            api_id=int(uuid.uuid4().int % 100000000),
            league_id=league_id,
            home_team=f"Local {uid}",
            away_team=f"Visitante {uid}",
            venue="Estadio Test",
            start_time=datetime.now(timezone.utc) + timedelta(days=2),
            status="NS",
        )
        session.add(fresh_match)
        await session.commit()

    match_id = str(fresh_match_id)

    # Listar partidos del torneo y verificar que el partido recién creado esté presente
    matches_resp = await client.get(
        f"/api/v1/tournaments/{tournament_id}/matches?next_days=7",
        headers=headers_a,
    )
    assert matches_resp.status_code == 200, matches_resp.text
    matches = matches_resp.json()
    assert any(m["id"] == match_id for m in matches)

    # 9. Usuario A y Usuario B pronostican
    # Usuario A predice 2 - 1 (acierto exacto)
    pred_a_resp = await client.post(
        f"/api/v1/matches/{match_id}/predictions?tournament_id={tournament_id}",
        headers=headers_a,
        json={"home_score": 2, "away_score": 1},
    )
    assert pred_a_resp.status_code == 201, pred_a_resp.text

    # Usuario B predice 0 - 2 (pronóstico fallido)
    pred_b_resp = await client.post(
        f"/api/v1/matches/{match_id}/predictions?tournament_id={tournament_id}",
        headers=headers_b,
        json={"home_score": 0, "away_score": 2},
    )
    assert pred_b_resp.status_code == 201, pred_b_resp.text

    # 10. Finalizar partido con resultado oficial 2 - 1
    result_resp = await client.post(
        f"/api/v1/matches/{match_id}/result",
        headers=headers_a,
        json={"home_score": 2, "away_score": 1},
    )
    assert result_resp.status_code == 200, result_resp.text

    # 11. Verificar Leaderboard
    leaderboard_resp = await client.get(
        f"/api/v1/tournaments/{tournament_id}/leaderboard",
        headers=headers_a,
    )
    assert leaderboard_resp.status_code == 200, leaderboard_resp.text
    leaderboard = leaderboard_resp.json()
    entries = leaderboard["entries"]
    assert len(entries) == 2

    # Usuario A debe ser Rank 1 con 10 puntos (5 exact + 3 winner + 2 diff)
    assert entries[0]["username"] == user_a_name
    assert entries[0]["total_points"] == 10
    assert entries[0]["rank"] == 1

    # Usuario B debe ser Rank 2 con 0 puntos
    assert entries[1]["username"] == user_b_name
    assert entries[1]["total_points"] == 0
    assert entries[1]["rank"] == 2

    # 12. Verificar estadísticas de perfil de Usuario A
    profile_a = await client.get("/api/v1/auth/me", headers=headers_a)
    assert profile_a.status_code == 200
    p_data = profile_a.json()
    assert p_data["current_streak"] == 1
    assert p_data["tournaments_played"] == 1
    assert p_data["accuracy_percentage"] == 100.0

    # 13. Historial de predicciones de Usuario A
    history_a = await client.get("/api/v1/users/me/predictions", headers=headers_a)
    assert history_a.status_code == 200
    hist = history_a.json()
    assert len(hist) >= 1
    assert hist[0]["points_earned"] == 10
    assert hist[0]["predicted_home"] == 2
    assert hist[0]["actual_home"] == 2
