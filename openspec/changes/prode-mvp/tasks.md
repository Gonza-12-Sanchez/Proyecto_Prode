# Tasks: Prode MVP

> Trazable a los 20 Requirements (`requirements.md`). Cada task referencia `R#`. Fases alineadas a `design.md` y `proposal.md`. Checkboxes `- [ ]` requeridos para tracking OpenSpec.

## 1. Auth & Perfil — R1, R2

- [ ] 1.1 Configurar proyecto FastAPI + Pydantic v2 + SQLAlchemy 2.0 async + Alembic + `core/config.py` (SECRET_KEY, DATABASE_URL, JWT_EXPIRE_HOURS=24, MOCK_MODE) — R1,R2
- [ ] 1.2 Crear tabla `users` con constraints (email ≤254 formato, username 3–30 `^[a-zA-Z0-9_-]{3,30}$`, password_hash, favorite_teams, current/longest_streak, is_premium) + índices email/username — R1 AC1–AC6, R2
- [ ] 1.3 Implementar `POST /api/v1/auth/register` con validación email formato, unicidad email/username, password 8–128, hash bcrypt, mensajes de conflicto específico — R1 AC1–AC6
- [ ] 1.4 Implementar `POST /api/v1/auth/login` con verificación credentials, error auth genérico si no coincide, retorno JWT (exp 24h), middleware `get_current_user` y expiración sesión 24h inactividad — R1 AC7–AC10
- [ ] 1.5 Implementar `GET /api/v1/users/me` y `PATCH /api/v1/users/me` (actualizar email con validación formato, favoritos ≤10, display username/email/torneos jugados/racha/stats) — R2 AC1–AC4, AC7–AC8
- [ ] 1.6 Implementar lógica de racha en `services/streaks.py` (consecutivos con >0 pts, reset a 0 si 0 pts, display actual y mejor histórica, solo scoreados) — R2 AC5–AC6, R18
- [ ] 1.7 Tests unitarios auth (registro válido/inválido, duplicado, login OK/fail, JWT exp 24h, validación username/password límites) — R1

## 2. Torneos & Invitaciones — R3, R4, R15, R16, R19

- [ ] 2.1 Crear tablas `leagues` (5 fijas), `tournaments` (invite_code CHAR(8) UNIQUE alfanum, max_participants IN (10,50), status Setup/Active/Completed, league_id FK, creator_id FK), `scoring_rules` (1:1 exact/correct_winner/goal_diff), `tournament_participants` PK compuesta + índice leaderboard — R3,R4,R15,R16,R19
- [ ] 2.2 Seed 5 ligas (Premier, La Liga, Serie A, Bundesliga, Ligue 1) con logo/nombre/external_id y `GET /api/v1/leagues` — R16
- [ ] 2.3 Implementar `POST /api/v1/tournaments` (nombre/descripción, selección 1 liga, Scoring_System configurable, validación Free 10 / Premium 50, creador = primer participante, status Setup) — R3 AC1–AC7, R19 AC1
- [ ] 2.4 Implementar generación `invite_code` 8 chars único global + `POST /api/v1/tournaments/join` con preview <2s (nombre, liga, reglas, ocupación) y validaciones código inválido / lleno (50) / ya participante — R4 AC1–AC6, R15 AC1–AC3
- [ ] 2.5 Implementar `GET /api/v1/tournaments` (mis torneos) y `GET /api/v1/tournaments/{id}` (detalle + estado + participantes + logo liga) — R4 AC7, R15 AC3–AC4, R16 AC4
- [ ] 2.6 Implementar `POST /api/v1/tournaments/{id}/start` (Setup→Active, bloquea config) + transiciones Setup editable / Active bloquea remove / Completed auto al finalizar todos los partidos — R15 AC5–AC6, R19 AC2–AC6
- [ ] 2.7 Validar contradicción límites: tests para Free 10 OK / 11 rechazado, Premium 50 OK / 51 rechazado, join en lleno → error "Tournament is full" — R3 AC4–AC5, R4 AC4–AC5
- [ ] 2.8 Tests integración torneos (crear con cada liga, código único, join <2s, duplicado, lleno, estados Setup/Active/Completed) — R3,R4,R15,R16,R19

## 3. Football API & Partidos — R5

- [ ] 3.1 Implementar `FootballPort` Protocol + `ApiFootballAdapter` (httpx timeout 30s, retry 3×/5s, raise tras 3 fallos) + `MockAdapter` con `app/mocks/*.json` por liga (fixtures realistas con start_time futuros/pasados) + factory por `MOCK_MODE` — R5 AC1,AC6,AC8
- [ ] 3.2 Crear tabla `matches` (external_id UNIQUE, league_id FK, home/away/venue, start_time, status NS/LIVE/FT/POSTPONED/CANCELLED, home_score/away_score) + índices (league_id,start_time), status, start — R5
- [ ] 3.3 Implementar `workers/fixtures_sync.py` cron cada 24h (pull por liga, upsert excluyendo incompletos sin team/date/time, log fallback_used) — R5 AC1,AC2,AC7
- [ ] 3.4 Implementar `workers/results_poller.py` cron cada 10min (poll `status=finished`, retrieve <10min, update matches <1min, excluir incompletos) — R5 AC3–AC4
- [ ] 3.5 Implementar `GET /api/v1/tournaments/{id}/matches?next=7d` (ventana 7 días, display team/date/time/venue, manejo "datos temporalmente no disponibles" si API cae tras 3 intentos) — R5 AC2,AC5–AC6
- [ ] 3.6 Configurar `core/scheduler.py` APScheduler (jobs 24h a 06:00 UTC y 10min) + lifespan en `main.py` + cache DB primaria y opcional Redis TTL — R5
- [ ] 3.7 Tests integración Football API (mock fixtures, retry/timeout, exclusión incompletos, ventana 7 días, mensaje no disponible) — R5 AC6–AC8

## 4. Predicciones, Scoring, Leaderboard, Historial, Rachas — R6, R7, R8, R17, R18

- [ ] 4.1 Crear tabla `predictions` con `UNIQUE(user_id,tournament_id,match_id)`, CHECK home/away ≥0, points_earned nullable, índices user_tournament/match/pending — R6,R7
- [ ] 4.2 Implementar `POST /api/v1/matches/{id}/predictions` y `PUT` editar (validar `start_time > now()`, rechazar si ya empezó, listar partidos por torneo, indicar si predicción enviada, lock permanente tras resultado) — R6 AC1–AC7
- [ ] 4.3 Implementar `services/scoring.py` función pura `score_prediction(pred, result, rules)->int` acumulativa (exact_score + correct_winner + goal_difference se suman; 0 si ningún criterio; idempotente) — R7 AC1–AC7
- [ ] 4.4 Implementar trigger scoring al finalizar partido: calcular puntos para todas las predictions del match, sumar a `tournament_participants.total_points`, mostrar puntos ganados — R7 AC1–AC2, AC8, AC10
- [ ] 4.5 Implementar recálculo leaderboard tras scoring + `GET /api/v1/tournaments/{id}/leaderboard` (orden puntos DESC, desempate accuracy %, muestra username/puntos/predicciones/accuracy, highlight usuario actual, update <5min) — R7 AC9, R8 AC1–AC6
- [ ] 4.6 Implementar `GET /api/v1/users/me/predictions` historial (cronológico recientes primero, predicted vs actual vs puntos, filtro por torneo, estado pending/scoreado, accuracy completados) — R17 AC1–AC6
- [ ] 4.7 Actualizar rachas tras scoring (incremento si >0 pts, reset a 0 si 0, solo completados/scoreados, display actual y mejor histórica en perfil) — R18 AC1–AC6, R2 AC5–AC6
- [ ] 4.8 Tests parametrizados scoring (exact 5+3+2=10, solo winner, solo diff, empate 0-0 vs 1-1, 0 pts, acumulativo, idempotencia, leaderboard desempate accuracy, rachas) — R7,R8,R17,R18
- [ ] 4.9 Tests integración predicciones (crear/editar OK antes inicio, rechazo tras inicio, lock tras FT, UNIQUE evita duplicado) — R6

## 5. Persistencia, Sync Offline, Testing & Docs — R20 + Transversal

- [ ] 5.1 Configurar `db/session.py` async_sessionmaker + transacciones; garantizar save predicción <2s y `GET /users/me/predictions` multi-dispositivo carga canónico backend — R20 AC1–AC2, AC7
- [ ] 5.2 Implementar estrategia offline: cliente cola local (SQLite/AsyncStorage) `queue=[{op,payload,ts}]`, sync al reconectar en orden ts, idempotencia por UNIQUE, header `X-Sync-Status` e indicador UI — R20 AC3–AC4, AC6
- [ ] 5.3 Implementar resolución conflictos server-wins para datos scoreados (`points_earned NOT NULL` preserva servidor; pending last-write-wins por updated_at) — R20 AC5
- [ ] 5.4 Tests persistencia & sync (save <2s, queue offline + sync, server-wins scored vs. overwrite pending, login otro dispositivo carga reciente, indicador sync) — R20
- [ ] 5.5 Suite pytest completa (unit + integración + scoring parametrizado + concurrencia predicciones) con `pytest-asyncio` + `httpx` + mocks Football API; cobertura scoring 100% — R7,R20,PND404
- [ ] 5.6 Seed data + colección Postman/Brutal + video demo <2min (registro→crear torneo código 8 chars→ver partidos 7d→pronosticar→scoring→leaderboard) — Transversal
- [ ] 5.7 Documentación: `README_Proyecto.md` §7 cómo correr, `.env.example`, `alembic upgrade head`, health `/health` y `/docs` Swagger — Transversal
- [ ] 5.8 Validación métricas piloto: endpoint `GET /admin/metrics` (D1/D7, completitud ≥60%, tiempo creación <2min p95, error scoring 0%, joins ≥90%) + logs estructurados — R20, §6 README

## 6. Validación Final & Entrega

- [ ] 6.1 Ejecutar `openspec validate --strict` y `openspec status --change prode-mvp --json` sin errores — Tooling
- [ ] 6.2 Verificar trazabilidad completa 20 Requirements (R1–R8,R15–R20 en MVP; R9–R14 documentados como Fase 2) en proposal/design/specs — Trazabilidad
- [ ] 6.3 Commit `docs(openspec): propose prode-mvp MVP $0` con `git add openspec/changes/prode-mvp/` — Entrega
