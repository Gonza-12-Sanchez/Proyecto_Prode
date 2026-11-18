# Design: Prode MVP — Arquitectura y Decisiones

## Context

Prode es una app B2C freemium de torneos privados de pronósticos (ex-Quiniela App, nombre provisorio). Ver `proposal.md — Why` para motivación y `requirements.md` (20 Requirements Kiro) para comportamiento canónico. El MVP es un **vertical slice $0** con dominio propio: Auth + Perfil + Crear/Unirse Torneo (código 8 chars) + Partidos (Football API) + Pronósticos + Scoring acumulativo + Leaderboard + Persistencia. Fuera: Chat (R12), Push (R13), Ads/Social (R11,R14). Stack decidido: **FastAPI + PostgreSQL relacional clásica + Adapter Mock**; 5 ligas: Premier, La Liga, Serie A, Bundesliga, Ligue 1. Contradicción resuelta: Free 10 / Premium 50 (100 diferido a Fase 2).

Estado actual: `openspec/specs/` vacío; greenfield. `requirements.md` y `README_Proyecto.md §§2–3` son la especificación funcional y arquitectónica previa.

## Goals / Non-Goals

**Goals:**
- Entregar vertical slice jugable de punta a punta en 6–8 semanas con scoring 0% error y preview torneo <2s, save predicción <2s, update leaderboard <5min.
- Arquitectura por capas testeable, con scoring como función pura e idempotente y workers desacoplados.
- Persistencia PostgreSQL con índices para joins frecuentes, transacciones ACID y sync offline con server-wins.
- Desacoplar proveedor Football API vía Adapter para operar en Mock $0 o Real sin cambiar dominio.
- Trazabilidad Requirement → Endpoint → Tabla → Spec delta.

**Non-Goals:**
- Chat (R12), Push/FCM con retry exponencial (R13), Ads cada 5 interacciones (R11), Social sharing (R14) y Premium 100 (R10 AC3) — backlog Fase 2.
- Multi-liga por torneo (N:M `tournament_leagues`) — MVP = 1 liga/torneo; 2–5 ligas simultáneas es mejora #2 Fase 2.
- Frontend móvil (React Native/Flutter) — el MVP backend expone OpenAPI; UI consume `/docs`.
- Multi-tenant RLS, sharding o microservicios — schema único PostgreSQL.
- Real-time WebSocket — Leaderboard por polling <5min en MVP.

## Decisions

### D1 — FastAPI (Python) vs. Java/Spring Boot vs. NestJS

**Decisión:** FastAPI + Pydantic v2 + SQLAlchemy 2.0 async.

**Rationale:** Async nativo para I/O-bound (Football API + DB) sin bloquear workers; validación declarativa (email 254, username regex, password 8–128) y OpenAPI/Swagger autogenerado útil para corrección TFI; `APScheduler` integrado para crons 24h/10min; ecosistema PostgreSQL maduro (Alembic). Curva de aprendizaje y boilerplate menores que Spring Boot para equipo TFI 6–8 semanas.

**Alternativas consideradas:** Java 21 + Spring Boot (desestimado: verboso, mayor overhead infra y sin ventaja async para este dominio) / Node/NestJS (desestimado: menor madurez en validación tipada vs. Pydantic y equipo con background Python).

### D2 — PostgreSQL relacional clásica vs. Firestore/Mongo vs. multi-tenant RLS

**Decisión:** PostgreSQL 15+ schema único, FKs explícitas, índices, transacciones; 9 tablas MVP (users, leagues, tournaments, tournament_participants, scoring_rules, matches, predictions, + chat_messages/notifications vacías Fase 2).

**Rationale:** Simplicidad TFI; ACID para scoring y leaderboard (recalc en transacción); `UNIQUE(user,tournament,match)` previene duplicados; índice `(tournament_id, total_points DESC, accuracy DESC)` para ranking; constraint `invite_code CHAR(8) UNIQUE` con check alfanum.

**Estructura de capas:**
```
app/
├── main.py                 # create_app(), lifespan(scheduler), middlewares, /health
├── core/
│   ├── config.py           # Settings pydantic-settings, SECRET_KEY, DATABASE_URL, MOCK_MODE
│   ├── security.py         # JWT (python-jose, exp 24h sliding), hash bcrypt (passlib), get_current_user
│   ├── errors.py           # handlers, códigos uniformes
│   └── scheduler.py        # APScheduler jobs 24h/10min
├── api/v1/
│   ├── auth.py             # POST /auth/register, /auth/login
│   ├── users.py            # GET/PATCH /users/me, /users/me/stats
│   ├── tournaments.py      # POST /tournaments, GET /tournaments/:id, POST /tournaments/join
│   ├── matches.py          # GET /tournaments/:id/matches?next=7d
│   ├── predictions.py      # POST/PUT /matches/:id/prediction  (o /predictions)
│   ├── leaderboard.py      # GET /tournaments/:id/leaderboard
│   └── history.py          # GET /users/me/predictions
├── models/                 # SQLAlchemy 2.0 (user, tournament, league, match, prediction, scoring_rule, participant)
├── schemas/                # Pydantic UserCreate/Out, TournamentCreate/Out, PredictionIn/Out, Leaderboard
├── services/
│   ├── scoring.py          # score_prediction(pred, result, rules)->int pura + recalc_leaderboard()
│   ├── tournament.py       # estados Setup→Active→Completed, validaciones 10/50
│   ├── streaks.py          # racha actual/mejor histórica
│   └── football_adapter.py # FootballPort protocol + ApiFootballAdapter + MockAdapter
├── workers/
│   ├── fixtures_sync.py    # job 24h
│   └── results_poller.py   # job 10min + trigger scoring <1min
├── mocks/                  # fixtures JSON por liga (fallback determinístico)
└── db/ {base, session, migrations}
```

### D3 — Football API Adapter + Mock + Workers

**Decisión:** Patrón Adapter con interfaz `FootballPort`:
```python
class FootballPort(Protocol):
    async def get_fixtures(self, league_id: int, next_days: int = 7) -> list[MatchDTO]: ...
    async def get_results(self, match_ids: list[int]) -> list[ResultDTO]: ...
class ApiFootballAdapter(FootballPort):  # httpx timeout 30s, retry 3×/5s
class MockAdapter(FootballPort):         # lee app/mocks/*.json, resultados determinísticos
```
Workers: `fixtures_sync` cada 24h (upsert excluyendo incompletos sin team/date/time) y `results_poller` cada 10min (si `status=FT` → update `home_score/away_score` <1min → trigger `score_match`). Cache primaria = tabla `matches`; opcional Redis TTL 10min para `<2s` preview por código y `<1s` p95 matches. Si Adapter falla tras 3 intentos → `MockAdapter` con `fallback_used=true` loggeado (no bloquea demo).

**Alternativa desestimada:** Llamada directa por request (rate limit, costo, latencia) o cron cada hora (exceso cuota). Consumo estimado Real Fase 2: ~42 req/día (~1260/mes) → Free 100/día sin margen, Pro $19/mes recomendado, pero MVP opera $0 con Mock.

### D4 — Límites Free 10 / Premium 50 (corrige contradicción 100)

**Decisión:** MVP valida `max_participants IN (10,50)` en `POST /tournaments` contra `users.is_premium`; `tournament_participants` cuenta vs. `max_capacity=50` en join (R4 AC4/AC5 corregido). Premium 100 (R3 AC5/R10 AC3) se habilita Fase 2 ampliando check a `(10,50,100)` y migración.

**Rationale:** Unifica contradicciones Req3 vs. Req4; evita over-engineering de capacidad sin demanda validada; coherente con métrica conversión simulada ≥15%.

### D5 — Seguridad: hash bcrypt + JWT 24h

**Decisión:** Passwords hasheados con `bcrypt` (passlib), nunca en claro; JWT HS256 con `exp = now+24h` (sliding o fixed según `core/security.py`), `SECRET_KEY` 32+ chars en env, `get_current_user` dependency en rutas Auth. Validaciones Pydantic: email formato estándar, username `^[a-zA-Z0-9_-]{3,30}$`, password 8–128.

### D6 — Offline queue + sync server-wins

**Decisión:** Cliente encola `[{op, payload, ts}]` en SQLite/AsyncStorage si sin red; al reconectar `POST /predictions` idempotente por `UNIQUE`; servidor preserva `points_earned NOT NULL` (ya scoreado) y resuelve conflictos pending por `updated_at` last-write-wins; header `X-Sync-Status` e indicador UI; `GET /users/me/predictions` carga canónico multi-dispositivo; save <2s.

### D7 — Modelo de datos (9 tablas, relaciones e índices)

DDL canónico en `README_Proyecto.md §3.2` (users, leagues, tournaments, tournament_participants, scoring_rules, matches, predictions, chat_messages, notifications). Claves:
- `tournaments.invite_code CHAR(8) UNIQUE CHECK alfanum` + índice para lookup <2s.
- `tournament_participants PK(tournament_id,user_id)` + índice `(tournament_id, total_points DESC, accuracy DESC)`.
- `predictions UNIQUE(user_id,tournament_id,match_id)` + índice parcial `WHERE points_earned IS NULL` para poller.
- `matches(league_id,start_time)` para ventana 7 días y cron.
- Estados `tournaments.status IN ('Setup','Active','Completed')` con transición manual `POST /tournaments/{id}/start`.

### Endpoints MVP (14)

| Método | Ruta | Auth | Req |
|---|---|---|---|
| POST | `/api/v1/auth/register` | No | R1 |
| POST | `/api/v1/auth/login` | No | R1 |
| GET | `/api/v1/users/me` | Sí | R2 |
| PATCH | `/api/v1/users/me` | Sí | R2 |
| POST | `/api/v1/tournaments` | Sí | R3 |
| POST | `/api/v1/tournaments/join` | Sí | R4 |
| GET | `/api/v1/tournaments` | Sí | R4 |
| GET | `/api/v1/tournaments/{id}` | Sí | R15,R19 |
| POST | `/api/v1/tournaments/{id}/start` | Sí (creador) | R19 |
| GET | `/api/v1/tournaments/{id}/matches` | Sí | R5 |
| POST | `/api/v1/matches/{id}/predictions` | Sí | R6 |
| PUT | `/api/v1/matches/{id}/predictions` | Sí | R6 |
| GET | `/api/v1/tournaments/{id}/leaderboard` | Sí | R8 |
| GET | `/api/v1/users/me/predictions` | Sí | R17 |
| GET | `/api/v1/leagues` | Sí | R16 |

Fase 2 añade: `GET/POST /tournaments/{id}/chat` (R12), `POST /notifications/subscribe` (R13), `POST /ads/*` (R11).

### Scoring acumulativo (R7) — función pura

```python
def score_prediction(pred: tuple[int,int], result: tuple[int,int], rules: ScoringRules) -> int:
    pts = 0
    if pred == result: pts += rules.exact_score          # implica winner y diff
    elif (pred[0]-pred[1]) == (result[0]-result[1]): pts += rules.goal_difference
    if (pred[0]-pred[1] > 0) == (result[0]-result[1] > 0) and \
       (pred[0]-pred[1] < 0) == (result[0]-result[1] < 0) and \
       (pred[0]==pred[1]) == (result[0]==result[1]):      # mismo signo/empate
        if pred != result: pts += rules.correct_winner    # si no fue exacto ya sumado
        # si fue exacto ya incluye winner+diff según reglas acumulativas
    return pts  # 0 si ningún criterio; idempotente, testeable parametrizado
```
En la implementación real, exacto otorga `exact+winner+diff` si los tres están definidos (exacto implica ganador y diferencia correctos); se suma a `tournament_participants.total_points` y dispara recálculo de accuracy, rank y streaks en transacción.

## Risks / Trade-offs

- **Football API caída / rate limit / datos incompletos →** Mitigación: timeout 30s + retry 3×/5s + cache DB + Mock fallback determinístico; fixtures cacheados 24h; mensaje "datos temporalmente no disponibles" sin crash (R5 AC6–AC8).
- **Baja retención B2C (D7 <25%) →** Mitigación: onboarding <2min, grupo piloto affinity, métrica D1/D7 como gate; Fase 2 push 2h reminder + achievements/comodín (#3/#4).
- **Scoring erróneo / reclamos →** Mitigación: función pura con tests parametrizados (exact/winner/diff/zero), auditoría `predicted vs actual vs points`, recálculo idempotente y transaccional.
- **Contradicción límites 10/50/100 →** Mitigación: decisión 10/50 MVP documentada y validada en API; 100 habilitado Fase 2 con migración.
- **Costos API escalan (5 ligas × polling) →** Mitigación: pull 24h + polling solo ventana 7 días (~42 req/día); Mock $0 para MVP produce costo 0.
- **Trade-off Mock vs. Real:** Mock = demo determinística y $0 pero sin frescura real; Real = datos vivos pero $19/mes y cuota — Adapter permite conmutar con `MOCK_MODE`.
- **Trade-off PostgreSQL vs. NoSQL:** SQL = transacciones y ranking eficiente pero schema rígido; NoSQL = flexibilidad pero sin ACID para scoring — se elige SQL.

## Migration Plan

1. **DB:** `alembic upgrade head` crea 9 tablas + índices; seed `python -m app.db.seed` carga 5 ligas y `app/mocks/*.json` (20+ partidos demo).
2. **Config:** `.env` con `MOCK_MODE=true` (MVP) o `FOOTBALL_API_KEY` + `MOCK_MODE=false` (Fase 2 Real); `SECRET_KEY`, `DATABASE_URL`, `FIXTURES_CRON_HOUR=6`, `RESULTS_POLL_SECONDS=600`.
3. **Deploy:** Railway/Render + Neon/Supabase free tier; `uvicorn app.main:app --reload` con lifespan que arranca APScheduler; `/health` y `/docs` verificables.
4. **Evolución Fase 2:** Migración `ALTER TABLE tournaments CHECK max_participants IN (10,50,100)`; crear `chat_messages`/`notifications` ya vacías no rompe MVP; Adapter conmuta sin migración de datos.
5. **Rollback:** Revertir migraciones `alembic downgrade -1`; workers idempotentes permiten re-ejecutar sin duplicar puntos; Mock fallback garantiza disponibilidad aunque API falle.

## Open Questions

- ¿Se usa `is_premium` booleano simple o `premium_expires_at` con job de expiración diaria para Fase 2? Respuesta MVP: booleano + `premium_expires_at` nullable (R10 AC6/AC7) suficiente; job expiración diferido a Fase 2.
- ¿FCM token se guarda en `users` o tabla `push_subscriptions`? Diferido a Fase 2 (R13).
- ¿Paginación para leaderboard/historial? MVP sin paginación (torneos ≤50, 7 días); paginación `limit/offset` en Fase 2 hardening.

---

## Propuestas de Mejora — Roadmap Fase 2 / Fase 3 (8 propuestas)

> Derivadas de gaps R12–R14, feedback piloto y oportunidades de retención no cubiertas por el vertical slice. Priorizadas por valor retención vs. esfuerzo. Ver `README_Proyecto.md §8`.

| # | Propuesta | Descripción | Valor retención | Esfuerzo | Fase |
|---|---|---|---|---|---|
| **1** | **Anti-trampa & Fair Play** | Bloqueo estricto edición al `start_time` + auditoría (`predicted_at`, `edited_at`, `ip_hash`) + heurística multi-cuenta (mismo dispositivo/IP, patrones idénticos) y panel reporte creador. Extiende R6/R7. | Alto: evita abandono por trampa; NPS +15. Crítico con premios. | Medio | **Fase 2** (P0 si hay reclamos) |
| **2** | **Modo Ligas Mixtas** | Torneo configurable 2–5 ligas simultáneas (vs. 1 actual R3/R16). Pool "Top 5 Europa" o "Champions + Premier". Migración `tournaments.league_id` → `tournament_leagues` N:M + workers multi-liga. | Alto: +40% partidos/semana, evita parones. | Medio | **Fase 2** |
| **3** | **Achievements / Gamificación** | Rachas extendidas (R18) + badges ("Pleno 3/3", "Invicto 5 fechas", "Verdugo del líder"), niveles Bronce→Leyenda, XP/ranking. Tablas `achievements` + `user_achievements` + triggers en `score_match`. | Muy Alto: D7 +10–15%, D30 +8%. Palanca freemium. | Medio | **Fase 2** |
| **4** | **Comodín / Doble Puntaje** | 1 comodín por fecha (configurable): duplica puntos del partido elegido, activado antes del inicio. Columna `is_joker` + `score×2` + validación 1/jornada. | Alto: decisión estratégica y debate grupal. | Bajo | **Fase 2** |
| **5** | **Head-to-Head (Duelos 1v1)** | Duelos semanales automáticos round-robin/ranking dentro del torneo; tabla H2H paralela. Tabla `h2h_matches` + cron emparejamientos + UI duelo. | Alto: rivalidad directa sostiene engagement fuera del top 3. | Medio | **Fase 2–3** |
| **6** | **Estadísticas Avanzadas pre-partido** | xG últimos 5, forma W/D/L, H2H, goles promedio local/visitante, lesiones. Datos `statistics`/`head2head` de Football API. Solo ayuda, no autoplay. | Medio-Alto: reduce fricción novato, mejora completitud ≥60%. | Medio | **Fase 2** |
| **7** | **Odds / Probabilidades** | Odds 1X2 y over/under como referencia ("Casa 60% / Empate 22% / Visita 18%"). Fuente API-Football / The Odds API. Toggle ocultar. Monetizable afiliación. | Medio: ancla confianza y conversación. | Bajo-Medio | **Fase 2** |
| **8** | **Offline-first mejorado (CRDT)** | Evolución R20 (cola + server-wins) a CRDT (Automerge/Yjs) o WatermelonDB + reintentos exponenciales, indicador conflicto y merge determinístico multi-dispositivo. | Medio: robustez en estadio/transporte sin señal. | Alto | **Fase 3** |

**Priorización sugerida:**
```
Fase 2 (4–6 sem): #1 Anti-trampa → #4 Comodín → #3 Achievements → #2 Ligas Mixtas
Fase 2 tardía: #6 Stats + #7 Odds (bundle ayuda al pronóstico)
Fase 3 (escala): #5 H2H → #8 Offline CRDT
```
> Criterio de corte: si piloto Fase 1 no alcanza D7 ≥25%, priorizar #3 + #4 (retención rápida) antes que #2/#8. Si hay reclamos de scoring, #1 es P0.

