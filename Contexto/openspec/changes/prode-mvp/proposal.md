# Proposal: Prode MVP — Torneos Privados de Pronósticos $0

## Why

Comunidades de amigos organizan quinielas/pronósticos de fútbol en grupos de WhatsApp + Excel + screenshots: sin reglas trazables, con errores de cálculo, pérdida de historial y sin ranking en tiempo real. **Prode** reemplaza esa dispersión por una plataforma única B2C freemium con scoring automático, leaderboard y persistencia — validando tracción por retención D1/D7 en lugar de piloto pagado B2B, con un MVP $0 (dominio propio + Mock Football API + free tiers).

## What Changes

- **Auth & Perfil (R1, R2):** Registro con email (≤254), username 3–30 alfanum `[a-zA-Z0-9_-]`, password 8–128; login con JWT expiración 24h inactividad; perfil con favoritos ≤10 equipos, racha, torneos jugados, accuracy 1 decimal y mejor posición.
- **Torneos & Invitaciones (R3, R4, R15, R16, R19):** Crear torneo con nombre/descripción, selección 1 liga de 5 (Premier, La Liga, Serie A, Bundesliga, Ligue 1), Scoring_System configurable (exact_score, correct_winner, goal_difference); límites Free 10 / Premium 50 (MVP, corrige contradicción 100→Fase 2); código invitación 8 chars alfanum único global, preview <2s, validaciones lleno/duplicado/inválido; link compartible + copiar código; estados Setup→Active (start manual, bloquea config)→Completed.
- **Football API & Partidos (R5, R16):** Adapter Football API (API-Football) con Mock fallback JSON local; workers cron pull fixtures cada 24h, polling resultados cada 10min y propagación <1min; ventana 7 días; retry 3×/5s, timeout 30s, exclusión partidos incompletos, cache DB.
- **Pronósticos, Scoring & Leaderboard (R6, R7, R8, R17, R18):** Pronosticar `home_score/away_score` editable hasta `start_time`, bloqueo tras inicio/finalizado; scoring acumulativo (exact + winner + diff se suman); recálculo leaderboard ordenado puntos DESC desempate accuracy, highlight usuario actual, update <5min; historial cronológico con predicted/actual/puntos y filtro torneo; rachas (streak = consecutivos con >0 pts, reset a 0, muestra actual y mejor histórica).
- **Persistencia & Sync (R20):** PostgreSQL relacional; save predicción <2s; cola local offline + sync al reconectar con idempotencia por `UNIQUE(user,tournament,match)` y resolución server-wins para datos scoreados; indicador sync; carga multi-dispositivo.
- **Infra $0:** FastAPI + PostgreSQL (Neon/Supabase free) + Mock mode (0 req externas); workers APScheduler; Pydantic v2, SQLAlchemy 2.0 async, Alembic.
- **BREAKING:** Límite Premium MVP es 50 (no 100). Req 3 AC5 (100) queda documentado como Fase 2 (Req 10).

## Capabilities

### New Capabilities

- `auth`: Autenticación y registro (R1) — email/username/password, validaciones, JWT 24h, hash bcrypt.
- `profile`: Perfil y estadísticas (R2) — favoritos, racha, torneos jugados, accuracy, mejor posición.
- `tournaments`: Creación, descubrimiento/join por código 8 chars, gestión invitaciones, multi-liga y estados (R3, R4, R15, R16, R19).
- `football-integration`: Integración Football API, Adapter + Mock, workers 24h/10min/1min, ventana 7 días, resiliencia (R5).
- `predictions`: Envío y edición de pronósticos con bloqueo temporal (R6).
- `scoring`: Cálculo acumulativo de puntos, leaderboard, historial y rachas (R7, R8, R17, R18).
- `persistence`: Persistencia PostgreSQL, cola offline y sincronización server-wins (R20).

### Modified Capabilities

<!-- No hay specs previas en openspec/specs — todas son nuevas para el MVP. Reqs R9–R14 (Free/Premium/Ads/Chat/Push/Social) quedan fuera de MVP/Fase 2. Contradicción 10/50/100 resuelta: 50 en MVP, 100 en Fase 2. -->

## Impact

- **Código:** Nuevo backend `app/` (api/core/models/schemas/services/workers/db), 9 tablas PostgreSQL, 14 endpoints REST bajo `/api/v1`, mocks `app/mocks/*.json` (5 ligas), migraciones Alembic, suite pytest.
- **APIs/Dependencias:** `httpx` async para Football API, `APScheduler` para crons, `python-jose` + `passlib/bcrypt` para auth, `asyncpg` + `SQLAlchemy 2.0`.
- **Sistemas:** Football API externa abstraída vía `FootballPort` (Adapter pattern); workers 24h/10m no bloquean request path; free tiers Railway/Render + Neon/Supabase sin costo.
- **Usuarios:** Free (10 pax/torneo, scoring básico, join ilimitado, leaderboard) y Premium (50 pax MVP, scoring avanzado — 100 en Fase 2). Ads (R11) y Chat/Push/Social (R12–R14) excluidos del MVP.
- **Métricas de éxito (piloto 10–15 usuarios, 14–21 días):** Retención D1 ≥40%, **D7 ≥25% (gate)**, DAU/WAU ≥0.4, **pronósticos completados ≥60%**, **tiempo creación torneo <2min (p95)**, **error scoring 0%**, joins exitosos ≥90%, NPS ≥30, conversión simulada free→premium ≥15%. Ver `README_Proyecto.md §6`.
- **No-goals MVP:** Chat 500/50 (R12), Push 2h/rank-jump con retry exponencial (R13), Social sharing (R14), Ads cada 5 interacciones (R9/R11), Premium 100 (R10).

## Requirements Traceability

| Dominio | Requirement | Estado MVP |
|---|---|---|
| Auth | R1, R2 | ✓ Incluido |
| Torneos | R3, R4, R15, R16, R19 | ✓ Incluido |
| Juego Core | R5, R6, R7, R8, R17, R18 | ✓ Incluido |
| Datos | R20 | ✓ Incluido |
| Social | R12, R14 | ◐ Fase 2 |
| Monetización | R9, R10, R11 | ◐ Fase 2 (límite 10/50 sí en MVP) |
| Notificaciones | R13 | ◐ Fase 2 |
