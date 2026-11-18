# ⚽ Prode — Torneos Privados de Pronósticos de Fútbol

![Status](https://img.shields.io/badge/Estado-MVP%20Vertical%20Slice-blue)
![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20FastAPI%20%7C%20PostgreSQL-336791)
![Modelo](https://img.shields.io/badge/Modelo-B2C%20Freemium-green)
![TFI](https://img.shields.io/badge/TFI-PND301%20%7C%20404%20%7C%20405-orange)
![Licencia](https://img.shields.io/badge/Licencia-Acad%C3%A9mica-lightgrey)

> **Resumen Ejecutivo:** Prode es una aplicación **B2C freemium** para crear y competir en **torneos privados de pronósticos** de fútbol real. Un usuario (Tournament_Creator) configura un torneo eligiendo liga, reglas de puntaje y límite de participantes; genera un **código de 8 caracteres** alfanuméricos y lo comparte por WhatsApp/redes. Los participantes se unen, pronostican resultados (marcador exacto) antes del inicio del partido y compiten en un **Leaderboard** ordenado por puntos totales con desempate por accuracy. El sistema integra datos reales vía **Football API externa** (5 ligas europeas) con sincronización automática, cálculo de puntaje acumulativo y persistencia relacional. El monetizado es **freemium con ads cada 5 interacciones** (Free hasta 10 participantes / Premium hasta 50). El MVP prioriza el flujo de valor completo — del registro al ranking — y deja Chat, Push y Social Sharing para Fase 2.

**Propuesta de valor central:** Crear una plataforma única con reglas trazables, scoring automático y ranking en tiempo real.

---

## Índice

1. [Justificación Académica (TFI)](#1-justificación-académica-tfi)
2. [Funcionalidades Técnicas Reales (Kiro — 20 Requirements)](#2-funcionalidades-técnicas-reales-kiro--20-requirements)
3. [Arquitectura Tecnológica Propuesta](#3-arquitectura-tecnológica-propuesta)
4. [Plan MVP y Roadmap](#4-plan-mvp-y-roadmap)
5. [Presupuesto — MVP $0 (Gratis) + Evolución Futura](#5-presupuesto--mvp-0-gratis--evolución-futura)
6. [Métricas de Validación TFI (B2C)](#6-métricas-de-validación-tfi-b2c)
7. [Stack y Cómo Empezar](#7-stack-y-cómo-empezar)
8. [Propuestas de Mejora (Fase 2+)](#8-propuestas-de-mejora-fase-2)

---

## 1. Justificación Académica (TFI)

### 1.1 Naturaleza de la idea: B2C propia vs. catálogo B2B

La guía `guia_tfi.md` propone 30 ideas TFI de tipo **B2B (Banco G y Banco A)** pensadas para maximizar probabilidad de convalidación académica. Este proyecto es una **idea propia B2C** y, por tanto, **no figura en el catálogo**. La defensa académica no se basa en negar los criterios de la guía, sino en **demostrar equivalencia rigurosa**: cada criterio B2B se mapea a un indicador B2C medible.

> **Tesis de defensa:** En B2C la tracción se valida por **retención y uso repetido**, no por contrato pagado. Un piloto con 10–15 usuarios reales que completan pronósticos jornada tras jornada es evidencia más fuerte que una carta de intención B2B sin uso.

### 1.2 Mapeo criterio por criterio (guia_tfi.md)

Cada criterio B2B de `guia_tfi.md` se traduce a un indicador B2C medible. La tabla siguiente detalla la equivalencia y su evidencia.

#### Tabla 1 — Mapeo criterio TFI (B2B → B2C)

| Criterio TFI (guia_tfi.md) | Exigencia original B2B | Cumplimiento B2C del proyecto | Evidencia / Entregable |
|---|---|---|---|
| **Dolor frecuente y presupuestado** | Problema que el cliente sufre semanalmente y por el que pagaría | **Dispersión de pronósticos en WhatsApp/Excel**: grupos de amigos que organizan torneos manualmente, sin scoring unificado, sin historial, con errores de cálculo y pérdida de mensajes. Dolor semanal (cada fecha) y alta frecuencia durante toda la temporada | Entrevistas previas + captura de grupos de WhatsApp + encuesta de dolor (N=15) |
| **Pagador visible** | Empresa cliente identificable que financia piloto | **Modelo freemium como proxy de disposición a pagar**: Free (ads) valida adquisición; Premium (torneos 50 pax + sin ads + scoring avanzado) valida conversión. El "piloto pagado" se sustituye por **cohorte de retención + tasa de conversión free→premium simulada** | Métricas: conversión, ARPU estimado, retención D1/D7/D30 |
| **MVP realizable en vertical** | Slice funcional que demuestra valor de punta a punta | **Vertical slice cerrado**: Registro → Crear/Unirse Torneo → Ver Partidos (API) → Pronosticar → Scoring automático → Leaderboard → Persistencia. Sin Chat/Push/Social en MVP, pero con flujo completo jugable | Demo jugable + colección Postman/Brutal + video <2 min |
| **Piloto con métricas** | Tiempo ahorrado, % aciertos, errores, adopción | **Métricas B2C equivalentes** (ver §6): Tiempo creación torneo <2 min, % pronósticos completados, error de scoring 0%, retención D1/D7, NPS | Dashboard de métricas + logs de scoring |
| **Integración de asignaturas PND** | PND301/302/303/401/404/405 | **Cobertura explícita** (ver §1.3) | Trazabilidad Requisito → Asignatura → Entregable |
| **Trazabilidad y aprobación humana** | Cada decisión automática es auditable y requiere OK humano | **Scoring auditable + predicciones bloqueadas al inicio + estados Setup/Active/Completed con transición manual del creador** | Historial de predicciones (predicted vs. actual vs. puntos), estados del torneo |
| **Riesgos y continuidad** | Plan de mitigación + visión post-MVP | **Riesgos identificados y mitigados** (ver §1.4) + roadmap Fase 2 claro | Matriz de riesgos + backlog Fase 2 |

### 1.3 Integración con asignaturas PND

La siguiente tabla vincula cada asignatura PND con su aporte concreto al proyecto y el artefacto que lo evidencia.

#### Tabla 2 — Aporte por asignatura PND

| Asignatura | Aporte al proyecto | Artefacto |
|---|---|---|
| **PND301 – Ingeniería de Requerimientos** | 20 Requirements con historias de usuario y criterios de aceptación formales (EARS: `THE System SHALL...`). Glosario y gestión de contradicciones (límite 50 vs. 100 resuelto en §2.1) | `requirements.md` + matriz de trazabilidad |
| **PND302 – Diseño de Software** | Arquitectura por capas, patrón Adapter para Football API, modelo relacional normalizado, diagrama ER y DDL | §3 de este README + DDL |
| **PND303 – Construcción / Backend** | FastAPI async + Pydantic + SQLAlchemy, workers cron, testing de scoring | `app/` + tests unitarios scoring |
| **PND401 – Gestión de Proyectos** | Plan MVP 6–8 semanas, roadmap Fase 1/2, criterios de Done, estimación de costos | §4 y §5 |
| **PND404 – Validación y Verificación / Testing** | Tests de scoring acumulativo, tests de integración API con retry/timeout, tests de concurrencia en predicciones | Suite `pytest` + mocks Football API |
| **PND405 – Fundamentos de Bases de Datos** | PostgreSQL relacional clásica, índices, transacciones, estrategia offline queue + sync con resolución `server-wins` para datos scoreados | §3.2 + scripts DDL |

### 1.4 Riesgos y mitigación

Riesgos principales detectados para el MVP y su plan de mitigación.

#### Tabla 3 — Matriz de riesgos y mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| **Football API caída / rate limit / datos incompletos** | Alta | Alto | Adapter + retry 3×/5s + timeout 30s + cache + **fallback Mock JSON local** (ver §3.3). Fixtures cacheados 24h |
| **Contradicción de requisitos (10/50/100 participantes)** | Ya detectada | Medio | Decisión MVP documentada: **Free 10 / Premium 50** (ver §2.1). Premium 100 queda para Fase 2 |
| **Baja retención B2C (usuarios no vuelven)** | Media | Alto | Recordatorio 2h antes (Fase 2 push), onboarding <2 min, grupo piloto de amigos/affinity, métrica D1/D7 como gate de continuidad |
| **Scoring erróneo / reclamos** | Baja | Alto | Cálculo acumulativo con tests parametrizados, auditoría por predicción (predicted/actual/puntos), recálculo idempotente |
| **Costos API escalan con 5 ligas** | Media | Medio | Pull cada 24h (no por request), polling resultados solo para partidos en ventana 7 días, mock para demo sin costo |

### 1.5 Continuidad

El proyecto está diseñado para **escalar sin re-arquitectura**: Fase 2 añade Chat (tabla `chat_messages`), Push (FCM), Ads y Premium 100 con el mismo esquema. La continuidad académica se sostiene si el MVP alcanza **retención D7 ≥ 25%** y **≥60% de pronósticos completados** en la cohorte piloto; de lo contrario se pivotea scoring o UX sin descartar la base técnica.

---

## 2. Funcionalidades Técnicas Reales (Kiro — 20 Requirements)

> Fuente canónica: `requirements.md` (requisitos_kiro.md). A continuación se agrupan los 20 requirements por dominio. Se marca con `✓ MVP` lo incluido en el vertical slice acordado y con `◐ Fase 2` lo diferido.

### 2.1 Nota de contradicción resuelta — Límites de participantes

`requirements.md` contiene dos límites distintos para Premium: **Req 3 AC5: 100** y **Req 4 AC4/AC5: 50**. La decisión MVP del equipo (usuario) es **Free 10 / Premium 50**. Este README adopta **10/50** como límite canónico del MVP; **100** se documenta como evolución Fase 2 (Req 10). El código valida `max_participants` contra el rol del creador en `POST /tournaments`.

### 2.2 Tabla por dominio

Los 20 requirements canónicos agrupados por dominio. Cada fila indica su estado en el MVP.

#### Tabla 4 — Requirements por dominio (20 Requirements Kiro)

| Dominio | Req | Funcionalidad | Detalle clave | Estado MVP |
|---|---|---|---|---|
| **Autenticación** | R1 | Registro y Login | Form con email (254 chars), username 3–30 alfanum.+`-`/`_`, password 8–128. Validación formato email, unicidad email/username, sesión expira **24h inactividad**. Session identifier (JWT) | ✓ MVP |
| | R2 | Perfil y Estadísticas | Username, email, equipos favoritos (≤10), torneos jugados, **racha** (consecutivos con puntos >0, reset a 0 si falla), total pronósticos, accuracy % (1 decimal), mejor posición histórica. Edición email con validación | ✓ MVP |
| **Torneos** | R3 | Creación de Torneos | Form: nombre/descripción, selección de **1 liga** (de 5), **Scoring_System** configurable (ver §2.3). Free 10 / Premium 50. Creador = primer participante. Estado inicial **Setup** | ✓ MVP |
| | R4 | Descubrimiento y Unión | Código invitación **8 chars alfanuméricos único** entre torneos activos. Preview <2s (nombre, liga, reglas, ocupación). Validaciones: código inválido, torneo lleno, ya participante. Listado "mis torneos" | ✓ MVP |
| | R15 | Gestión de Invitaciones | Link compartible + copiar código, listar participantes, expulsar participantes solo en **Setup** (bloqueado en Active) | ✓ MVP (sin push) |
| | R16 | Multi-Liga | 5 ligas soportadas: **Premier League, La Liga, Serie A, Bundesliga, Ligue 1**. Torneo = 1 liga (no multi-liga por torneo). Logo + nombre en detalle | ✓ MVP |
| | R19 | Estados del Torneo | **Setup** (editable reglas/aforo) → **Active** (start manual del creador, config bloqueada) → **Completed** (todos los partidos finalizados y scoreados). Estado visible | ✓ MVP |
| **Juego (Core)** | R5 | Integración Football API | Pull fixtures **cada 24h** por liga; resultado final **<10 min** tras `finished`; update en torneos **<1 min**; ventana visible **próximos 7 días**; **retry 3×/5s**, **timeout 30s**, exclusión de partidos incompletos (sin team/date/time) | ✓ MVP |
| | R6 | Pronosticar | Listar partidos por torneo, enviar `home_score`/`away_score`. **Editable hasta inicio del partido**, rechazado si ya empezó, bloqueo permanente tras resultado | ✓ MVP |
| | R7 | Scoring y Cálculo de Puntos | **Acumulativo** (ver §2.3). Recálculo de Leaderboard tras cada partido scoreado | ✓ MVP |
| | R8 | Leaderboard | Ranking **puntos desc**, desempate **accuracy %**, muestra username/puntos/pronósticos/accuracy, highlight usuario actual, update **<5 min** tras scoring | ✓ MVP |
| | R17 | Historial de Predicciones | Lista cronológica (recientes primero), muestra predicted vs. actual vs. puntos, filtro por torneo, estado pending/scoreado, accuracy de completados | ✓ MVP |
| | R18 | Rachas (Streaks) | Racha = consecutivos con **>0 puntos**, reset a 0 si 0 puntos. Solo predicciones completadas/scoreadas. Muestra racha actual y mejor histórica en perfil | ✓ MVP |
| **Social** | R12 | Chat de Torneo | Interfaz por torneo, broadcast, orden cronológico, **500 chars** por mensaje, carga **últimos 50** al abrir, notificación si chat abierto | ◐ Fase 2 |
| | R14 | Compartir Social | Botón share en Perfil y Leaderboard top 3, mensaje con stats + código invitación, destinos FB/Twitter/IG/WhatsApp, imagen con posición | ◐ Fase 2 |
| **Monetización** | R9 | Tier Gratuito | Scoring básico, Free 10 pax, join ilimitado, ver leaderboard/stats, **ads cada 5 interacciones** | ◐ Fase 2 (ads diferidos, límite 10 ya en MVP) |
| | R10 | Suscripción Premium | Upgrade vía pago, **50 pax (MVP) → 100 Fase 2**, scoring avanzado, sin ads, expiración → downgrade Free | ◐ Fase 2 |
| | R11 | Publicidad | Integración ad platform, contador page_view / prediction / leaderboard_refresh, reset tras ad, **degradación elegante si ad platform cae** | ◐ Fase 2 |
| **Notificaciones** | R13 | Push Notifications | Recordatorio **2h antes** si sin pronóstico, resultado+pts, salto **±3 ranks**, invitación. Toggle en perfil, vía FCM/APNs, **retry exponencial 1m/5m/15m** (3 intentos), cancelación si horario cambia | ◐ Fase 2 |
| **Datos** | R20 | Persistencia y Sync Offline | PostgreSQL backend, guardado predicción **<2s**, **cola local offline** + sync al reconectar, **server-wins para datos scoreados**, indicador de sync, carga multi-dispositivo | ✓ MVP (sync offline = cola local + server-wins) |
| | R5/R20 | Datos de Partidos | Ver §3.3 tolerancia a fallos | ✓ MVP |

### 2.3 Scoring acumulativo — Regla de negocio central (R7)

Cada torneo define su `Scoring_System` con tres valores (ej. `exact_score=5, correct_winner=3, goal_difference=2`). Al finalizar un partido se compara `prediction(home, away)` vs. `match(home, away)`:

#### Tabla 5 — Reglas de scoring acumulativo (R7)

| Condición | Puntos otorgados | Ejemplo (pred 2-1 vs. real 2-1) |
|---|---|---|
| **Marcador exacto** (`home==real_home && away==real_away`) | `exact_score` | ✓ 5 pts |
| **Ganador correcto** (signo `home-away` igual) | `correct_winner` | ✓ 3 pts |
| **Diferencia de gol correcta** (`(home-away)==(real_home-real_away)` y no exacto) | `goal_difference` | ✓ si aplica |

**Acumulativo:** Si se dan varias condiciones, **se suman**. Un 2-1 exacto otorga `5+3+2 = 10` si el sistema define los tres (porque exacto implica ganador y diferencia correctos). Un 1-0 vs. 2-1 (mismo ganador, distinta diferencia) otorga solo `correct_winner`. Un 0-0 vs. 1-1 (empate, diferencia 0 en ambos) otorga `goal_difference` (+ `correct_winner` según definición de empate como ganador). Predicción sin aciertos = 0.

> Implementación: función pura `score_prediction(pred, result, rules) -> int` con tests parametrizados; idempotente y re-ejecutable tras corrección de resultado. Puntos se suman a `tournament_participants.total_points` y disparan recálculo de leaderboard y rachas.

### 2.4 Football API — Tolerancia a fallos (R5)

- **Pull fixtures:** `GET /fixtures?league=X&next=7` cada **24h** (cron worker).
- **Resultados:** polling cada **≤10 min** para partidos con `status=finished`, propagación a `matches` **<1 min**.
- **Resiliencia:** `timeout 30s` por request, **retry 3× con intervalo 5s**, si falla → mensaje "datos temporalmente no disponibles" (no crash). Partidos incompletos (sin team/date/time) se excluyen.
- **Cache:** fixtures cacheados en DB + opcional Redis/memory para <2s en preview de torneo por código.

### 2.5 Límites y validaciones clave

- **Código invitación:** 8 alfanuméricos, `UNIQUE WHERE status != 'Completed'` (o global único según Req 4 AC1; se recomienda único global para simplicidad).
- **Capacidad:** `Free max 10 / Premium max 50` (MVP). Validación en creación y en join.
- **Predicción:** `home_score, away_score >=0` integers, `match.start_time > now()` para aceptar/editar.
- **Chat (Fase 2):** 500 chars, 50 mensajes iniciales, orden cronológico.
- **Sesión:** expira tras 24h inactividad (sliding window o JWT exp 24h).

---

## 3. Arquitectura Tecnológica Propuesta

### 3.1 Backend — Python FastAPI

**Justificación del stack:**

La tabla siguiente resume por qué FastAPI es el framework elegido para el backend.

#### Tabla 6 — Justificación del stack FastAPI

| Criterio | Por qué FastAPI |
|---|---|
| **Async nativo** | `async/await` para I/O-bound (Football API, DB) sin bloquear workers; polling de resultados concurrente |
| **Pydantic v2** | Validación declarativa (email 254, username regex, password 8–128) y schemas OpenAPI auto-generados |
| **Docs OpenAPI** | `/docs` (Swagger) y `/redoc` sin costo, útil para corrección TFI y testing manual |
| **Workers** | Fácil integración con `APScheduler` / `Celery` / `arq` para crons 24h y polling 10 min |
| **Ecosistema PostgreSQL** | SQLAlchemy 2.0 async + Alembic migraciones, maduro y bien documentado |

**Estructura de carpetas propuesta:**

```
app/
├── main.py                 # create_app(), lifespan (scheduler), middlewares
├── core/
│   ├── config.py           # Settings (pydantic-settings, env vars)
│   ├── security.py         # JWT, hash (passlib/bcrypt), deps get_current_user
│   ├── errors.py           # handlers, códigos de error uniformes
│   └── scheduler.py        # APScheduler: jobs 24h y 10min
├── api/
│   ├── v1/
│   │   ├── auth.py         # POST /auth/register, /auth/login
│   │   ├── users.py        # GET/PATCH /users/me, /users/me/stats
│   │   ├── tournaments.py  # POST /tournaments, GET /tournaments/:id, POST /join
│   │   ├── matches.py      # GET /tournaments/:id/matches?next=7d
│   │   ├── predictions.py  # POST/PUT /matches/:id/prediction
│   │   ├── leaderboard.py  # GET /tournaments/:id/leaderboard
│   │   └── history.py      # GET /users/me/predictions
│   └── deps.py             # Depends(get_db), Depends(get_current_user)
├── models/
│   ├── user.py
│   ├── tournament.py
│   ├── league.py
│   ├── match.py
│   ├── prediction.py
│   └── scoring_rule.py
├── schemas/
│   ├── user.py             # UserCreate, UserOut, Login
│   ├── tournament.py       # TournamentCreate, TournamentOut, JoinByCode
│   ├── prediction.py       # PredictionIn, PredictionOut
│   └── leaderboard.py
├── services/
│   ├── scoring.py          # score_prediction() pura + recalc_leaderboard()
│   ├── tournament.py       # lógica estados Setup→Active→Completed
│   ├── streaks.py
│   └── football_adapter.py # Adapter Football API (ver §3.3)
├── workers/
│   ├── fixtures_sync.py    # job 24h
│   └── results_poller.py   # job 10min + update <1min
└── db/
    ├── base.py
    ├── session.py          # async_sessionmaker
    └── migrations/         # Alembic
```

**Endpoints clave (MVP):**

Endpoints implementados en el vertical slice del MVP.

#### Tabla 7 — Endpoints clave del MVP

| Método | Ruta | Auth | Descripción | Req |
|---|---|---|---|---|
| `POST` | `/api/v1/auth/register` | No | Registro email/username/password | R1 |
| `POST` | `/api/v1/auth/login` | No | Login → JWT (exp 24h) | R1 |
| `GET` | `/api/v1/users/me` | Sí | Perfil + racha + stats | R2 |
| `PATCH` | `/api/v1/users/me` | Sí | Actualizar email / favoritos (≤10) | R2 |
| `POST` | `/api/v1/tournaments` | Sí | Crear torneo (liga + scoring + 10/50) | R3 |
| `POST` | `/api/v1/tournaments/join` | Sí | Unirse por `code` (8 chars) | R4 |
| `GET` | `/api/v1/tournaments` | Sí | Mis torneos | R4 |
| `GET` | `/api/v1/tournaments/{id}` | Sí | Detalle + estado + participantes | R15,R19 |
| `POST` | `/api/v1/tournaments/{id}/start` | Sí (creador) | Setup → Active | R19 |
| `GET` | `/api/v1/tournaments/{id}/matches` | Sí | Partidos próximos 7 días | R5 |
| `POST` | `/api/v1/matches/{id}/predictions` | Sí | Crear/editar pronóstico (bloqueo al inicio) | R6 |
| `GET` | `/api/v1/tournaments/{id}/leaderboard` | Sí | Ranking + desempate accuracy | R8 |
| `GET` | `/api/v1/users/me/predictions` | Sí | Historial + filtro torneo | R17 |
| `GET` | `/api/v1/leagues` | Sí | Listado 5 ligas | R16 |

Fase 2 añade: `GET/POST /tournaments/{id}/chat`, `POST /notifications/subscribe`, `GET /ads/config`.

### 3.2 Base de Datos — PostgreSQL relacional clásica

> **Estructura híbrida profesional (desde refactor `database/` vs `app/`):** Todo lo de BD vive en `database/` (responsabilidad **Datos**: `database/connection.py`, `database/models/`, `database/alembic/`, `database/init/init_db.sql`, `database/seeds/`), separado de la lógica pura del backend en `app/` (responsabilidad **Backend**: `app/api/`, `app/services/`, `app/workers/`, `app/schemas/`, `app/core/` sin DB). El backend **nunca** hace `create_all`; el esquema se crea por DDL o Alembic. Para DBeaver: abrir y ejecutar `database/init/init_db.sql` (incluye `CREATE EXTENSION pgcrypto;` y las 9 tablas) y luego `database/seeds/leagues.sql` para las 5 ligas. Ver `database/README.md` para flujo completo.

**Decisión:** PostgreSQL relacional clásica (no multi-tenant complejo, no RLS). Un único schema, FKs explícitas, índices para joins frecuentes. Justificación: simplicidad TFI, transacciones ACID para scoring, y compatibilidad con hosting managed gratuito.

**Diagrama textual (ER simplificado):**

```
users 1──∞ tournament_participants ∞──1 tournaments 1──1 scoring_rules
  │                    │                    │
  │                    │                    ├──∞ matches (via league)
  │                    │                    └──∞ predictions (via matches)
  │                    │
  │                    └──── tournament status: Setup/Active/Completed
  │
  ├──∞ predictions
  ├──∞ chat_messages (Fase 2)
  └──∞ notifications (Fase 2)

leagues 1──∞ matches 1──∞ predictions
leagues 1──∞ tournaments
```

**DDL resumido (MVP + Fase 2 opcional):**

```sql
-- 1. users
CREATE TABLE users (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email             VARCHAR(254) UNIQUE NOT NULL CHECK (email ~* '^[^@]+@[^@]+\.[^@]+$'),
  username          VARCHAR(30)  UNIQUE NOT NULL CHECK (username ~ '^[a-zA-Z0-9_-]{3,30}$'),
  password_hash     TEXT NOT NULL,
  favorite_teams    TEXT[] DEFAULT '{}', -- JSON o FK a teams si se normaliza; MVP: array IDs
  current_streak    INT DEFAULT 0,
  longest_streak    INT DEFAULT 0,
  is_premium        BOOLEAN DEFAULT FALSE,
  premium_expires_at TIMESTAMPTZ,
  created_at        TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- 2. leagues (5 fijas + extensibles)
CREATE TABLE leagues (
  id          SMALLINT PRIMARY KEY, -- ej 39=Premier, 140=La Liga...
  name        VARCHAR(80) NOT NULL,
  country     VARCHAR(80),
  logo_url    TEXT,
  external_id INT UNIQUE -- id en Football API
);

-- 3. tournaments
CREATE TABLE tournaments (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name            VARCHAR(120) NOT NULL,
  description     TEXT,
  league_id       SMALLINT NOT NULL REFERENCES leagues(id),
  creator_id      UUID NOT NULL REFERENCES users(id),
  invite_code     CHAR(8) UNIQUE NOT NULL CHECK (invite_code ~ '^[A-Za-z0-9]{8}$'),
  max_participants SMALLINT NOT NULL CHECK (max_participants IN (10,50,100)),
  status          VARCHAR(10) NOT NULL DEFAULT 'Setup' CHECK (status IN ('Setup','Active','Completed')),
  created_at      TIMESTAMPTZ DEFAULT now(),
  started_at      TIMESTAMPTZ,
  completed_at    TIMESTAMPTZ
);
CREATE INDEX idx_tournaments_invite ON tournaments(invite_code);
CREATE INDEX idx_tournaments_creator ON tournaments(creator_id);
CREATE INDEX idx_tournaments_league ON tournaments(league_id);

-- 4. tournament_participants (N:M)
CREATE TABLE tournament_participants (
  tournament_id UUID NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
  user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  total_points  INT DEFAULT 0,
  predictions_count INT DEFAULT 0,
  accuracy      NUMERIC(5,2) DEFAULT 0, -- % 0-100
  rank          INT,
  joined_at     TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (tournament_id, user_id)
);
CREATE INDEX idx_participants_user ON tournament_participants(user_id);
CREATE INDEX idx_participants_leaderboard ON tournament_participants(tournament_id, total_points DESC, accuracy DESC);

-- 5. scoring_rules (1:1 con tournament)
CREATE TABLE scoring_rules (
  tournament_id   UUID PRIMARY KEY REFERENCES tournaments(id) ON DELETE CASCADE,
  exact_score     INT NOT NULL DEFAULT 5 CHECK (exact_score >=0),
  correct_winner  INT NOT NULL DEFAULT 3 CHECK (correct_winner >=0),
  goal_difference INT NOT NULL DEFAULT 2 CHECK (goal_difference >=0)
);

-- 6. matches
CREATE TABLE matches (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  external_id   BIGINT UNIQUE, -- id Football API
  league_id     SMALLINT NOT NULL REFERENCES leagues(id),
  home_team     VARCHAR(80) NOT NULL,
  away_team     VARCHAR(80) NOT NULL,
  venue         VARCHAR(120),
  start_time    TIMESTAMPTZ NOT NULL,
  status        VARCHAR(20) NOT NULL DEFAULT 'NS' CHECK (status IN ('NS','LIVE','FT','POSTPONED','CANCELLED')),
  home_score    SMALLINT,
  away_score    SMALLINT,
  created_at    TIMESTAMPTZ DEFAULT now(),
  updated_at    TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_matches_league_time ON matches(league_id, start_time);
CREATE INDEX idx_matches_status ON matches(status);
CREATE INDEX idx_matches_start ON matches(start_time);

-- 7. predictions
CREATE TABLE predictions (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  tournament_id UUID NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
  match_id      UUID NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
  home_score    SMALLINT NOT NULL CHECK (home_score >=0),
  away_score    SMALLINT NOT NULL CHECK (away_score >=0),
  points_earned SMALLINT, -- NULL = pending, 0..n = scoreado
  created_at    TIMESTAMPTZ DEFAULT now(),
  updated_at    TIMESTAMPTZ DEFAULT now(),
  UNIQUE (user_id, tournament_id, match_id) -- 1 pronóstico por usuario/partido/torneo
);
CREATE INDEX idx_predictions_user_tournament ON predictions(user_id, tournament_id);
CREATE INDEX idx_predictions_match ON predictions(match_id);
CREATE INDEX idx_predictions_pending ON predictions(match_id) WHERE points_earned IS NULL;

-- 8. chat_messages (Fase 2 - opcional en MVP, crear tabla vacía)
CREATE TABLE chat_messages (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tournament_id UUID NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
  user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  body          VARCHAR(500) NOT NULL CHECK (char_length(body) <= 500),
  created_at    TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_chat_tournament_time ON chat_messages(tournament_id, created_at DESC);

-- 9. notifications (Fase 2)
CREATE TABLE notifications (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type          VARCHAR(30) NOT NULL, -- reminder_2h, result, rank_jump, invite
  payload       JSONB NOT NULL,
  is_read       BOOLEAN DEFAULT FALSE,
  created_at    TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_notifications_user ON notifications(user_id, created_at DESC);
```

**Relaciones e índices clave:**

- `tournaments.invite_code` único + índice para lookup <2s (Req 4 AC2).
- `tournament_participants` PK compuesta + índice `(tournament_id, total_points DESC, accuracy DESC)` para leaderboard.
- `predictions` UNIQUE `(user_id, tournament_id, match_id)` evita duplicados (Req 4 AC6 / R6).
- `matches(league_id, start_time)` para ventana 7 días y cron.
- `predictions WHERE points_earned IS NULL` para poller de scoring.

**Estrategia de persistencia offline (R20):**

```
[móvil]  cola local (SQLite/AsyncStorage) --offline--> queue = [{op, payload, ts}]
   │                      │
   │ reconexión           │ POST /predictions (idempotente por UNIQUE)
   ▼                      ▼
[backend]  PostgreSQL transacción  --conflicto-->  server-wins si points_earned IS NOT NULL
              (datos ya scoreados no se sobrescriben)
   │
   └── indicador sync: header X-Sync-Status / polling GET /sync/status
```

- Predicción se guarda en DB **<2s** (Req 20 AC2).
- Sin red: se encola localmente; al reconectar se sincroniza en orden `ts`, con **idempotencia** por constraint único.
- Conflictos: si el servidor ya scoreó la predicción (`points_earned NOT NULL`), se preserva versión del servidor (server-wins, Req 20 AC5). Si aún es pending, last-write-wins por `updated_at`.
- Login en otro dispositivo: `GET /users/me/predictions` carga estado canónico del backend.

### 3.3 Integración Football API — Adapter + Worker + Fallback Mock

**Patrón Adapter:** desacopla el dominio del proveedor externo. El dominio solo ve `FootballPort`.

```
[Football API Externa] ──HTTP──> [FootballAdapter] ──DTO interno──> [Services/Workers]
        │                              │
        │ timeout 30s                  │ retry 3×/5s + cache + mock fallback
        │                              │
        └──────────> [mocks/fixtures.json] (JSON local si API cae)
```

```python
# app/services/football_adapter.py (esquemático)
class FootballPort(Protocol):
    async def get_fixtures(self, league_id: int, next_days: int = 7) -> list[MatchDTO]: ...
    async def get_results(self, match_ids: list[int]) -> list[ResultDTO]: ...

class ApiFootballAdapter(FootballPort):
    BASE = "https://v3.football.api-sports.io"
    def __init__(self, api_key: str): ...
    async def _get(self, path, params):
        for attempt in range(3):
            try:
                async with httpx.AsyncClient(timeout=30) as c:
                    r = await c.get(path, params=params, headers={"x-apisports-key": self.key})
                    r.raise_for_status()
                    return r.json()
            except (Timeout, HTTPError):
                if attempt == 2: raise
                await asyncio.sleep(5)

class MockAdapter(FootballPort):
    """Fallback: lee app/mocks/fixtures.json y genera resultados determinísticos"""
    async def get_fixtures(self, league_id, next_days=7): return load_json(...)
```

**Workers (APScheduler):**

Jobs programados que mantienen sincronizados los fixtures y resultados.

#### Tabla 8 — Workers y cron jobs

| Job | Cron | Acción |
|---|---|---|
| `fixtures_sync` | Cada **24h** (ej. 06:00 UTC) | `for league in 5: adapter.get_fixtures(league)` → upsert en `matches` (excluye incompletos) |
| `results_poller` | Cada **10 min** | Para `matches WHERE status='NS' AND start_time < now()`: `adapter.get_results()` → si `FT`, update `home_score/away_score/status='FT'` **<1 min** → trigger `scoring_service.score_match(match_id)` |
| `leaderboard_refresh` | Tras cada `score_match` | Recalcula `total_points`, `accuracy`, `rank` y `streaks` en transacción |

**Cache:** `matches` en DB es la cache primaria; opcional `Redis` TTL 10 min para `GET /matches` si se quiere <1s p95.

**Elección recomendada — API-Football (api-sports.io):**

- Cubre las 5 ligas exigidas, incluye `fixtures`, `livescore` y `teams`.
- Plan **Free: 100 req/día** → insuficiente para 5 ligas × 24h + polling 10 min en producción.
- Plan **Pro: ~$19/mes (7500 req/día)** → suficiente para MVP (ver §5).
- Alternativas: Football-Data.org (Free 10 req/min, menos ligas), Sportmonks. Se abstraen vía Adapter.

**Fallback Mock (demo sin costo):**

```
app/mocks/
├── fixtures_premier.json
├── fixtures_laliga.json
├── fixtures_seriea.json
├── fixtures_bundesliga.json
└── fixtures_ligue1.json
```

Si `FootballAdapter` falla tras 3 intentos, el `fixtures_sync` conmuta a `MockAdapter` y loggea `fallback_used=true`. Esto **no bloquea la demo** ante el profesor y permite validar scoring/leaderboard sin gastar cuota.

---

## 4. Plan MVP y Roadmap

### 4.1 Fase 1 — MVP Vertical Slice (6–8 semanas) — **Alcance actual**

Plan semanal del MVP. Cada entregable se vincula a sus requirements.

#### Tabla 9 — Cronograma MVP Fase 1

| Semana | Entregable | Reqs |
|---|---|---|
| 1–2 | Auth + Perfil + DB + migraciones + CI | R1, R2, R20 |
| 3 | Torneos: creación, scoring config, invite code 8 chars, join, estados Setup/Active | R3, R4, R15, R19 |
| 4 | Football API Adapter + workers 24h/10min + mock fallback + catálogo 5 ligas | R5, R16 |
| 5 | Pronósticos (crear/editar/bloqueo) + validaciones | R6 |
| 6 | Scoring acumulativo + Leaderboard + Historial + Rachas | R7, R8, R17, R18 |
| 7 | Persistencia <2s + cola offline + sync server-wins + tests integrales | R20 |
| 8 | Pulido, seed data, demo script, métricas y README (este archivo) | — |

**Incluido en MVP:** Auth, Perfil, Crear/Unirse Torneo, Ver Partidos (7 días), Pronosticar (editable hasta inicio), Scoring acumulativo, Leaderboard (desempate accuracy), Historial, Rachas, Estados Setup/Active/Completed, Persistencia PostgreSQL + cola offline + sync. **Límites 10/50**.

**Fuera de MVP (Fase 2):** Chat 500/50, Push 2h/recordatorio/rank-jump con retry exponencial, Ads cada 5 interacciones, Social Sharing, Premium 100.

### 4.2 Fase 2 — Post-MVP (4–6 semanas adicionales)

Funcionalidades diferidas a la Fase 2, fuera del vertical slice.

#### Tabla 10 — Backlog Fase 2

| Feature | Req | Notas |
|---|---|---|
| Chat por torneo | R12 | WebSocket o polling corto, 500 chars, 50 msgs, tabla `chat_messages` |
| Push Notifications | R13 | FCM, jobs 2h reminder + result + rank±3, retry 1m/5m/15m |
| Ads + Premium 100 | R9–R11 | AdMob/web ads cada 5 interacciones, upgrade a 100 pax, sin ads premium |
| Social Sharing | R14 | OG images, deep links con invite code |
| Hardening | — | Rate limiting, paginación, observabilidad (logs/metrics), tests E2E |

### 4.3 Criterios de Done (MVP)

- [ ] Registro/login con validaciones + JWT exp 24h + tests
- [ ] Crear torneo con liga + scoring + código 8 chars único + join <2s preview + validaciones lleno/duplicado
- [ ] Fixtures visibles 7 días, pull 24h, retry 3×/5s, timeout 30s, mock fallback funcional sin API key
- [ ] Pronóstico editable hasta `start_time`, bloqueado después, `UNIQUE(user,tournament,match)`
- [ ] Scoring acumulativo con tests parametrizados (exact/winner/diff), error 0% en suite, recálculo leaderboard <5 min
- [ ] Leaderboard ordenado puntos→accuracy, highlight usuario, historial y rachas correctas
- [ ] Persistencia: save <2s, cola offline + sync, server-wins para scoreados, multi-dispositivo
- [ ] Seed de 5 ligas + 20 partidos mock + 2 torneos demo + colección Postman

---

## 5. Presupuesto — MVP $0 (Gratis) + Evolución Futura

> **MVP 100% gratuito ($0/mes).** El vertical slice se construye con **Mock local + free tiers** y el **dominio propio ya adquirido ($0)**. No hay gasto obligatorio para demo, corrección TFI ni piloto 10–15 usuarios. Los costos solo aparecen en **Fase 2 al escalar a datos reales sin mock**.

### 5.1 MVP Fase 1 — Costo $0

El MVP funciona sin API externa de pago. `MOCK_MODE=true` sirve fixtures desde `app/mocks/*.json` y toda la infraestructura corre en capas gratuitas.

#### Tabla 11 — Costo MVP Fase 1 (todos $0)

| Concepto | Costo MVP | Notas |
|---|---|---|
| **Football API — Mock local** | **$0/mes** | `MockAdapter` lee `app/mocks/*.json` (5 ligas). Cero requests externos, demo determinística |
| **Hosting Backend (FastAPI)** | **$0/mes** | Free tier Railway / Render / Fly.io (512 MB, sleep permitido para demo) |
| **PostgreSQL managed** | **$0/mes** | Free tier Supabase / Neon / Railway Postgres (0.5–1 GB, suficiente para MVP) |
| **Dominio propio** | **$0/mes** | Ya adquirido por el equipo — no se presupuesta |
| **Push Notifications (FCM)** | **$0/mes** | Solo Fase 2; Firebase Cloud Messaging es gratuito e ilimitado |
| **Ads / Social SDK** | **$0/mes** | Solo Fase 2; revenue, no costo |
| **Total MVP Fase 1** | **$0/mes** | **100% funcional para demo TFI y piloto 10–15 usuarios** |

> **Cómo se logra $0:** `FOOTBALL_API_KEY` vacío o `MOCK_MODE=true` → ningún consumo de cuota. Backend y DB en free tier. Dominio propio elimina el único gasto fijo que otros MVPs sí pagan ($12/año).

### 5.2 Fase 2 — Costos futuros opcionales (solo al escalar)

Estos costos **no aplican al MVP**. Solo se activan cuando se desactiva el mock (`MOCK_MODE=false`) y se opera con datos reales en producción continua.

#### Tabla 12 — Costos futuros al escalar a datos reales (Fase 2)

| Concepto | Costo Fase 2 | Notas |
|---|---|---|
| **Football API — Plan Pro (API-Football)** | **~$19/mes** | 7 500 req/día. Reemplaza al Mock. Necesario solo si se quiere polling real 24h/10 min sin límite. Mercado: $15–30/mes |
| **Hosting Backend sin sleep** | **$5–10/mes** | Hobby plan Railway/Render/Fly para evitar cold start. Free tier sigue siendo opción si se tolera sleep |
| **PostgreSQL prod (opcional)** | **$7–10/mes** | Solo si se supera el free tier (1 GB). Supabase/Neon free alcanza para cientos de torneos |
| **Dominio** | **$0/mes** | Ya adquirido |
| **Total Fase 2 (con API real)** | **$19–30/mes** | Rango completo con API Pro + hosting hobby |

> **Regla de activación:** Mientras `MOCK_MODE=true`, el costo es $0. El paso a $19/mes es una decisión explícita del equipo al iniciar piloto con datos reales continuos o producción.

## 5.3 Modelo B2C + B2B – Torneos Corporativos

El MVP ahora se ofrece tanto a usuarios finales (B2C) como a empresas que desean organizar torneos internos para sus empleados (B2B). Cada empresa puede crear torneos privados, gestionar participantes y acceder a reportes de engagement.

### Unit‑Economics (B2B)

| Concepto | Coste operativo (€/mes) | Ingreso estimado (€/mes) | Margen |
|---|---|---|---|
| Licencia empresa (hasta 50 usuarios) | **200 €** | **200 €** | 0 % |
| Hosting + soporte premium | 5 € | 0 € | -5 % |
| Ads / ingresos por clic (opcional) | 0 € | 50 € | +∞ |

### Métricas de Validación & KPI

Se reutilizan las métricas definidas en la sección **6. Métricas de Validación TFI (B2C)**, aplicándolas al segmento B2B (ej. retención D7 empresarial, número de torneos creados por empresa, satisfacción NPS corporativo).

### Matriz de Riesgos & Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Caída API Football | Alta | Alto | Adapter con fallback mock y circuit‑breaker (ya implementado). |
| Baja retención B2B | Media | Alto | Programa de onboarding, demo personalizada, soporte 24 h. |
| Errores de scoring | Baja | Alto | Tests unitarios extensos, auditoría de puntuaciones, recalculo idempotente. |
| Escalado de usuarios | Media | Medio | Arquitectura basada en FastAPI async + PostgreSQL escalable; plan de recursos en la nube. |

### 5.3 Estimación de consumo API (5 ligas) — Referencia para Fase 2

Si se activa la API real, el consumo estimado es el siguiente. Con Mock este consumo es **$0**.

#### Tabla 13 — Consumo estimado API-Football (solo Fase 2)

| Operación | Frecuencia | Req/día | Req/mes |
|---|---|---|---|
| Pull fixtures 5 ligas | 1×/24h ×5 | 5 | 150 |
| Polling resultados (ventana 7 días, ~30 partidos/sem) | cada 10 min solo partidos en juego (~6h/día ×6 req/h) | ~36 | ~1 080 |
| Leagues/teams metadata | semanal | ~1 | ~30 |
| **Total estimado** | | **~42/día** | **~1 260/mes** |

→ **Free 100/día alcanzaría** pero sin margen para reintentos. Con retry 3× y Fase 2, el **Pro $19/mes** da holgura 75×. En MVP con Mock este cálculo es solo informativo.

### 5.4 Estrategia mock para no bloquear demo

1. **Desarrollo y corrección TFI:** `MOCK_MODE=true` → `MockAdapter` lee `app/mocks/*.json` (fixtures realistas por liga, con `start_time` futuros y pasados para probar scoring). Cero costo, cero dependencia externa, demo determinística.
2. **Piloto 10–15 usuarios:** Se mantiene `MOCK_MODE=true` con actualización manual de `fixtures.json` cada fecha. Solo si se quiere validar con datos reales continuos se pasa a `MOCK_MODE=false` + API Pro ($19).
3. **Producción:** Adapter con **circuit breaker**: si API falla → sirve cache DB + mock, y reintenta en background (no bloquea UX).

### 5.5 Horas de desarrollo (estimación TFI)

Estimación de esfuerzo académico (no monetizado). La infra sigue siendo $0 en MVP.

#### Tabla 14 — Horas estimadas por rol

| Rol | Horas MVP (6–8 sem) |
|---|---|
| Backend (FastAPI + DB + workers) | 60–80 h |
| Frontend móvil (si aplica, React Native/Flutter) | 60–80 h |
| Integración API + scoring + tests | 20–30 h |
| **Total** | **140–190 h** |

> Costo académico: horas del equipo (no monetizado). Costo infra MVP: **$0/mes** (Mock + free tiers + dominio propio).

---

## 6. Métricas de Validación TFI (B2C)

> Reemplazan el "piloto pagado" B2B por un **piloto de retención** con cohorte 10–15 usuarios (amigos, compañeros, comunidad futbolera). Ventana de medición: **2–3 fechas (14–21 días)**.

#### Tabla 15 — KPIs de validación B2C (piloto retención)

| KPI | Definición | Meta MVP | Cómo se mide | Criterio TFI que reemplaza |
|---|---|---|---|---|
| **Retención D1** | % usuarios que vuelven al día siguiente del registro | ≥40% | `users.created_at` vs. `last_login` | Adopción piloto |
| **Retención D7** | % usuarios activos a los 7 días | **≥25%** (gate de continuidad) | DAU/WAU, `predictions.created_at` | Adopción + tracción |
| **DAU/WAU** | Daily Active / Weekly Active | ≥0.4 | Sesiones + predicciones/día | Uso frecuente (dolor semanal) |
| **% pronósticos completados** | `predicciones realizadas / partidos disponibles` por usuario/fecha | **≥60%** | `predictions / matches` en ventana 7d | Tiempo/errores evitados |
| **Tiempo creación torneo** | Desde "Crear" hasta código generado | **<2 min** | Logs `POST /tournaments` p95 | Tiempo ahorrado |
| **% usuarios que completan 3 pronósticos** | Al menos 3 predictions en primer torneo | ≥70% | `COUNT(predictions) >=3` | Activación |
| **Error de scoring** | Predicciones con puntos mal calculados | **0%** | Suite parametrizada + auditoría `predicted vs actual vs points` | % aciertos / errores |
| **% joins por código exitosos** | `joins OK / intentos join` | ≥90% | `POST /join` 200 vs. 4xx | Fricción |
| **NPS / Satisfacción** | "¿Recomendarías la app?" 0–10 | ≥30 (NPS) / ≥4.0/5 | Encuesta post-fecha (Google Form) | Validación cualitativa |
| **Conversión simulada Free→Premium** | % que dice "pagaría por 50 pax/sin ads" | ≥15% intención | Encuesta + toggle premium mock | Pagador visible (proxy) |

**Instrumentación mínima MVP:**

- Logs estructurados en `predictions`, `tournaments`, `users.last_login`.
- Endpoint `GET /admin/metrics` (solo dev) con agregados D1/D7, completitud, p95 creación.
- Encuesta post-piloto (5 preguntas, ver `docs/encuesta_nps.md` si se crea).

**Criterio de éxito TFI:** Si **D7 ≥25% + completitud ≥60% + error scoring 0%**, el MVP se considera **validado como sustituto de piloto pagado** y habilita Fase 2. Si no, se itera UX/scoring sin descartar arquitectura.

---

## 8. Propuestas de Mejora (Fase 2+)

> Roadmap de evolución post-MVP. Propuestas derivadas de gaps en los 20 Requirements, feedback de piloto B2C y oportunidades de retención no cubiertas por el vertical slice (Chat R12, Push R13, Ads R11, Scoring avanzado R10). Priorizadas por valor de retención vs. esfuerzo.

### 8.1 Resumen por categorías

| Categoría | Propuestas | Objetivo principal |
|---|---|---|
| **A. Integridad & Fair Play** | #1 Anti-trampa | Confianza y legitimidad del ranking |
| **B. Variedad de Competición** | #2 Ligas Mixtas, #5 Head-to-Head | Rejugabilidad y personalización |
| **C. Engagement & Gamificación** | #3 Achievements, #4 Comodín | Retención D7/D30 y viralidad |
| **D. Inteligencia & Datos** | #6 Estadísticas avanzadas, #7 Odds | Reducir fricción al pronosticar |
| **E. Experiencia Técnica** | #8 Offline-first mejorado | Robustez y accesibilidad |

### 8.2 Detalle de propuestas

#### Tabla 16 — Propuestas Fase 2+ (8 iniciativas)

| # | Propuesta | Descripción | Valor para retención | Esfuerzo | Fase sugerida |
|---|---|---|---|---|---|
| **1** | **Anti-trampa & Fair Play** | Bloqueo estricto de edición al `start_time` + log de auditoría (`predicted_at`, `edited_at`, `ip_hash`) + detección heurística de múltiples cuentas (mismo dispositivo/IP, patrones de voto idénticos) y panel de reporte para el creador. Extiende R6/R7 con trazabilidad. | **Alto:** Evita abandono por percepción de trampa; NPS +15 pts. Crítico para torneos con premios. | **Medio** | **Fase 2** (inmediato post-MVP) |
| **2** | **Modo Ligas Mixtas** | Torneo configurable con 2–5 ligas simultáneas (vs. 1 liga actual R3/R16). El creador elige pool de partidos (ej. "Top 5 Europa" o "Fecha Champions + Premier"). Leaderboard unificado, filtro por liga. | **Alto:** +40% partidos disponibles/semana, evita semanas muertas por parón de liga. | **Medio** (cambio `tournaments.league_id` → `tournament_leagues` N:M + workers multi-liga) | **Fase 2** |
| **3** | **Sistema de Achievements / Gamificación** | Rachas extendidas (R18) + insignias ("Pleno 3/3", "Invicto 5 fechas", "Verdugo del líder"), niveles (Bronce→Leyenda), XP por pronóstico y ranking. UI de perfil con vitrina de badges y progreso. | **Muy Alto:** Loop de progresión diario; D7 +10–15%, D30 +8%. Palanca freemium para Premium. | **Medio** (tabla `achievements` + `user_achievements` + triggers en `score_match`) | **Fase 2** |
| **4** | **Pronósticos con Comodín / Doble Puntaje** | 1 comodín por fecha/jornada (configurable por torneo): duplica puntos del partido elegido. Debe activarse antes del inicio. Estado `is_joker` en `predictions`, scoring `×2`. | **Alto:** Decisión estratégica que aumenta debate en grupo y retorno cada fecha. | **Bajo** (columna boolean + regla `score×2` + validación 1/jornada) | **Fase 2** |
| **5** | **Modo Head-to-Head (Duelos 1v1)** | Duelos semanales automáticos (matchmaking round-robin o ranking) dentro del torneo. Cada fecha se resuelve el H2H por puntos de la jornada; tabla H2H paralela al leaderboard global. | **Alto:** Rivalidad directa sostiene engagement aunque el usuario esté lejos del top 3. | **Medio** (tabla `h2h_matches` + cron de emparejamientos + UI duelo) | **Fase 2–3** |
| **6** | **Estadísticas Avanzadas para Pronosticar** | Panel pre-partido con xG últimos 5, forma (W/D/L), historial H2H, goles promedio local/visitante y lesiones clave. Datos derivados de Football API `statistics`/`head2head`. Solo ayuda, no autoplay. | **Medio-Alto:** Reduce fricción del novato, mejora % pronósticos completados (KPI ≥60%). | **Medio** (ingesta `team_stats` + cache + UI) | **Fase 2** |
| **7** | **Importar Fixtures Reales con Odds / Probabilidades** | Mostrar odds 1X2 y over/under como referencia ("Casa 60% / Empate 22% / Visita 18%"). Fuente: odds de API-Football o The Odds API. Toggle "ocultar odds" para puristas. | **Medio:** Ancla de confianza y conversación; ayuda a pronosticar sin decidir por el usuario. Monetizable vía afiliación. | **Bajo-Medio** (campo `odds` en `matches` + adapter + UI badge) | **Fase 2** |
| **8** | **Modo Offline-first Mejorado (CRDT / Sync Robusto)** | Evolución de R20 (cola local + server-wins) a sincronización con CRDT (Automerge/Yjs) o `WatermelonDB` + cola con reintentos exponenciales, indicador de conflicto y merge determinístico multi-dispositivo. | **Medio:** Experiencia resiliente en estadio/transporte sin señal; reduce pérdida de pronósticos. | **Alto** (re-arquitectura sync, pruebas de partición) | **Fase 3** |

### 8.3 Priorización sugerida

```
Fase 2 (próximas 4–6 semanas): #1 Anti-trampa → #4 Comodín → #3 Achievements → #2 Ligas Mixtas
Fase 2 tardía: #6 Stats + #7 Odds (bundle "ayuda al pronóstico")
Fase 3 (escala): #5 H2H → #8 Offline CRDT (requiere base estable)
```

> **Criterio de corte:** Si piloto Fase 1 no alcanza D7 ≥25%, priorizar #3 + #4 (retención rápida) antes que #2/#8. Si hay reclamos de scoring, #1 es P0.

---

## 7. Stack y Cómo Empezar

### 7.1 Stack

Stack tecnológico del MVP y su versión sugerida.

#### Tabla 17 — Stack tecnológico

| Capa | Tecnología | Versión sugerida |
|---|---|---|
| Backend | **Python + FastAPI** | Python 3.11+, FastAPI 0.110+ |
| Validación | Pydantic v2 + pydantic-settings | 2.x |
| ORM / Migraciones | SQLAlchemy 2.0 (async) + Alembic | 2.0+ |
| DB | **PostgreSQL 15+** | 15 o 16 |
| Auth | JWT (python-jose) + passlib/bcrypt | — |
| Scheduler | APScheduler 3.x (o Celery si se escala) | 3.10+ |
| HTTP | httpx (async) | 0.27+ |
| Tests | pytest + pytest-asyncio + httpx | — |
| API externa | API-Football (api-sports.io) + Mock fallback | v3 |
| Push (Fase 2) | Firebase Admin SDK (FCM) | — |

### 7.2 Requisitos previos

- Python 3.11+
- PostgreSQL 15+ (local o Docker)
- `git`, `pip`/`poetry` o `uv`

### 7.3 Instalación

```bash
# 1. Clonar y entorno
git clone <repo> quiniela-app && cd quiniela-app
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt
# o con uv: uv sync

# 2. Variables de entorno
cp .env.example .env
# Editar .env con tus valores (ver §7.4)

# 3. Base de datos (Docker opcional)
docker run --name quiniela-pg -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=quiniela -p 5432:5432 -d postgres:16
# o usa tu Postgres local y crea DB `quiniela`

# 4. Migraciones
alembic upgrade head

# 5. Seed (ligas + partidos mock)
python -m app.db.seed  # carga 5 ligas y fixtures de app/mocks/

# 6. Run
uvicorn app.main:app --reload --port 8000
# Docs: http://localhost:8000/docs
# Health: http://localhost:8000/health
```

### 7.4 Variables de entorno (`.env`)

```ini
# App
APP_ENV=dev                 # dev | prod
SECRET_KEY=change-me-32chars
JWT_EXPIRE_HOURS=24

# DB
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/quiniela

# Football API
FOOTBALL_API_PROVIDER=api-football   # api-football | mock
FOOTBALL_API_KEY=                    # vacío = mock automático
FOOTBALL_API_BASE=https://v3.football.api-sports.io
MOCK_MODE=true                       # true = usa app/mocks/*.json aunque haya key

# Scheduler
FIXTURES_CRON_HOUR=6                 # UTC hour para pull 24h
RESULTS_POLL_SECONDS=600             # 600 = 10 min

# Fase 2 (opcional)
FIREBASE_CREDENTIALS_JSON=
AD_PROVIDER=
```

### 7.5 Comandos útiles

```bash
# Tests (incluye scoring acumulativo)
pytest -v
pytest tests/test_scoring.py -v   # casos exact/winner/diff/zero

# Lint / format
ruff check app && ruff format app

# Crear torneo de prueba (requiere JWT)
curl -X POST http://localhost:8000/api/v1/tournaments \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Amigos Premier","league_id":39,"scoring_rules":{"exact_score":5,"correct_winner":3,"goal_difference":2}}'

# Unirse por código
curl -X POST http://localhost:8000/api/v1/tournaments/join \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"invite_code":"A1B2C3D4"}'
```

### 7.6 Estructura del repositorio (resumen)

```
.
├── app/                # backend FastAPI (ver §3.1)
├── app/mocks/          # fixtures JSON por liga (fallback)
├── alembic/            # migraciones
├── tests/              # pytest (scoring, api, sync)
├── requirements.md     # 20 requirements canónicos
├── guia_tfi.md         # (referencia, no versionada si es privada)
├── README_Proyecto.md  # este archivo
└── .env.example
```

---

## Anexo — Trazabilidad Requirement → Endpoint → Tabla

Matriz que vincula cada requirement con sus endpoints y tablas.

#### Tabla 18 — Trazabilidad Requirement → Endpoint → Tabla

| Req | Endpoint(s) | Tabla(s) |
|---|---|---|
| R1 | `POST /auth/register`, `POST /auth/login` | `users` |
| R2 | `GET/PATCH /users/me` | `users` |
| R3 | `POST /tournaments` | `tournaments`, `scoring_rules`, `tournament_participants` |
| R4 | `POST /tournaments/join`, `GET /tournaments` | `tournaments`, `tournament_participants` |
| R5 | `GET /tournaments/{id}/matches` + workers | `matches`, `leagues` |
| R6 | `POST /matches/{id}/predictions` | `predictions` |
| R7 | (interno `score_match`) | `predictions`, `tournament_participants` |
| R8 | `GET /tournaments/{id}/leaderboard` | `tournament_participants` |
| R12 | `GET/POST /tournaments/{id}/chat` (F2) | `chat_messages` |
| R13 | `POST /notifications/*` (F2) | `notifications` |
| R20 | (transversal) | todas + cola local |

---

*Documento listo para entrega TFI. Cubre justificación B2C frente a guia_tfi.md, 20 requirements de requirements.md, arquitectura FastAPI+PostgreSQL, presupuesto MVP $0 (Mock + free tiers + dominio propio) y métricas de validación por retención.*
