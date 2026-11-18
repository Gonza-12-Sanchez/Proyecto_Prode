-- [DATABASE] init/init_db.sql - DDL completo para DBeaver (9 tablas).
-- Ubicación: database/init/init_db.sql
-- Responsabilidad: Capa DATABASE - Crea extensión pgcrypto y las 9 tablas con CHECK, UNIQUE, FKs e índices para pegar directo en DBeaver.
-- Usa: PostgreSQL 15+, ejecutado vía DBeaver SQL Editor o psql \i
-- No hace: No inserta datos (ver seeds/leagues.sql), solo estructura. Backend nunca hace create_all.

-- =========================================================
-- Prode - Quiniela MVP - DDL Completo (híbrido database/ vs app/)
-- Generado desde database/models/*.py (SQLAlchemy 2.0 async)
-- 9 tablas: users, leagues, tournaments, tournament_participants, scoring_rules, matches, predictions, chat_messages, notifications
-- Ejecutar en DB vacía "quiniela"
-- =========================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(254) UNIQUE NOT NULL CHECK (email ~* '^[^@]+@[^@]+\.[^@]+$'),
    username VARCHAR(30) UNIQUE NOT NULL CHECK (username ~ '^[a-zA-Z0-9_-]{3,30}$'),
    hashed_password TEXT NOT NULL,
    is_premium BOOLEAN NOT NULL DEFAULT FALSE,
    premium_expires_at TIMESTAMPTZ,
    current_streak INT NOT NULL DEFAULT 0,
    longest_streak INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- 2. leagues (5 fijas + extensibles)
CREATE TABLE IF NOT EXISTS leagues (
    id SMALLINT PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    country VARCHAR(80),
    logo_url TEXT,
    api_id INT UNIQUE
);

-- 3. tournaments
CREATE TABLE IF NOT EXISTS tournaments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(120) NOT NULL,
    description TEXT,
    league_id SMALLINT NOT NULL REFERENCES leagues(id),
    creator_id UUID NOT NULL REFERENCES users(id),
    invite_code CHAR(8) UNIQUE NOT NULL CHECK (invite_code ~ '^[A-Za-z0-9]{8}$'),
    max_participants SMALLINT NOT NULL CHECK (max_participants IN (10,50,100)),
    status VARCHAR(10) NOT NULL DEFAULT 'Setup' CHECK (status IN ('Setup','Active','Completed')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS idx_tournaments_invite ON tournaments(invite_code);
CREATE INDEX IF NOT EXISTS idx_tournaments_creator ON tournaments(creator_id);
CREATE INDEX IF NOT EXISTS idx_tournaments_league ON tournaments(league_id);

-- 4. tournament_participants (N:M)
CREATE TABLE IF NOT EXISTS tournament_participants (
    tournament_id UUID NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    total_points INT NOT NULL DEFAULT 0,
    predictions_count INT NOT NULL DEFAULT 0,
    accuracy NUMERIC(5,2) NOT NULL DEFAULT 0,
    rank INT,
    PRIMARY KEY (tournament_id, user_id)
);
CREATE INDEX IF NOT EXISTS idx_participants_user ON tournament_participants(user_id);
CREATE INDEX IF NOT EXISTS idx_participants_leaderboard ON tournament_participants(tournament_id, total_points DESC, accuracy DESC);

-- 5. scoring_rules (1:1 con tournament)
CREATE TABLE IF NOT EXISTS scoring_rules (
    tournament_id UUID PRIMARY KEY REFERENCES tournaments(id) ON DELETE CASCADE,
    exact_score INT NOT NULL DEFAULT 5 CHECK (exact_score >= 0),
    correct_winner INT NOT NULL DEFAULT 3 CHECK (correct_winner >= 0),
    goal_difference INT NOT NULL DEFAULT 2 CHECK (goal_difference >= 0)
);

-- 6. matches
CREATE TABLE IF NOT EXISTS matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    api_id BIGINT UNIQUE,
    league_id SMALLINT NOT NULL REFERENCES leagues(id),
    home_team VARCHAR(80) NOT NULL,
    away_team VARCHAR(80) NOT NULL,
    venue VARCHAR(120),
    start_time TIMESTAMPTZ NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'NS' CHECK (status IN ('NS','LIVE','FT','POSTPONED','CANCELLED')),
    home_score SMALLINT,
    away_score SMALLINT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_matches_league_time ON matches(league_id, start_time);
CREATE INDEX IF NOT EXISTS idx_matches_status ON matches(status);
CREATE INDEX IF NOT EXISTS idx_matches_start ON matches(start_time);

-- 7. predictions
CREATE TABLE IF NOT EXISTS predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tournament_id UUID NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
    match_id UUID NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    home_score SMALLINT NOT NULL CHECK (home_score >= 0),
    away_score SMALLINT NOT NULL CHECK (away_score >= 0),
    points_earned SMALLINT,
    is_scored BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (user_id, tournament_id, match_id)
);
CREATE INDEX IF NOT EXISTS idx_predictions_user_tournament ON predictions(user_id, tournament_id);
CREATE INDEX IF NOT EXISTS idx_predictions_match ON predictions(match_id);
CREATE INDEX IF NOT EXISTS idx_predictions_pending ON predictions(match_id) WHERE points_earned IS NULL;

-- 8. chat_messages (Fase 2)
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tournament_id UUID NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    body VARCHAR(500) NOT NULL CHECK (char_length(body) <= 500),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_chat_tournament_time ON chat_messages(tournament_id, created_at DESC);

-- 9. notifications (Fase 2)
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(30) NOT NULL,
    payload JSONB NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id, created_at DESC);

-- Verificación rápida post-ejecución:
-- SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename;
-- Debe listar 9 tablas.
