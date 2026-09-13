-- [DATABASE] seeds/demo_data.sql - Datos demo opcionales para probar scoring y leaderboard.
-- Ubicación: database/seeds/demo_data.sql
-- Responsabilidad: Capa DATABASE - Inserta usuario demo, torneo demo y partidos de ejemplo. Útil para demo sin Football API real.
-- Usa: tablas users, tournaments, tournament_participants, scoring_rules, matches (leagues debe existir)
-- No hace: No reemplaza migraciones ni DDL, solo datos de prueba borrables.

-- Usuario demo (password hash bcrypt para "demo1234" - reemplazar en prod)
INSERT INTO users (id, email, username, hashed_password, is_premium, current_streak, longest_streak)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'demo@prode.local',
    'demo_user',
    '$2b$12$demo_hash_placeholder_replace_me',
    false,
    2,
    5
) ON CONFLICT (id) DO NOTHING;

-- Torneo demo (requiere leagues 39 cargada)
INSERT INTO tournaments (id, name, description, league_id, creator_id, invite_code, max_participants, status)
VALUES (
    '10000000-0000-0000-0000-000000000001',
    'Demo Premier Amigos',
    'Torneo demo para validar flujo completo',
    39,
    '00000000-0000-0000-0000-000000000001',
    'DEMO1234',
    10,
    'Setup'
) ON CONFLICT (id) DO NOTHING;

INSERT INTO scoring_rules (tournament_id, exact_score, correct_winner, goal_difference)
VALUES ('10000000-0000-0000-0000-000000000001', 5, 3, 2)
ON CONFLICT (tournament_id) DO NOTHING;

INSERT INTO tournament_participants (tournament_id, user_id, total_points, predictions_count, accuracy)
VALUES ('10000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 0, 0, 0)
ON CONFLICT (tournament_id, user_id) DO NOTHING;

-- Partidos demo (futuros, ventana 7 días)
INSERT INTO matches (id, api_id, league_id, home_team, away_team, venue, start_time, status)
VALUES
    ('20000000-0000-0000-0000-000000000001', 9001, 39, 'Arsenal', 'Manchester City', 'Emirates Stadium', now() + interval '1 day', 'NS'),
    ('20000000-0000-0000-0000-000000000002', 9002, 39, 'Liverpool', 'Chelsea', 'Anfield', now() + interval '2 days', 'NS'),
    ('20000000-0000-0000-0000-000000000003', 9003, 140, 'Real Madrid', 'Barcelona', 'Santiago Bernabeu', now() + interval '3 days', 'NS')
ON CONFLICT (id) DO NOTHING;

-- Verificación:
-- SELECT * FROM tournaments WHERE invite_code='DEMO1234';
-- SELECT * FROM matches WHERE league_id=39 ORDER BY start_time;
