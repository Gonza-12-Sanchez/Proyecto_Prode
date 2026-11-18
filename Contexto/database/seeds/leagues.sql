-- [DATABASE] seeds/leagues.sql - Seeds de las 5 ligas europeas (MVP).
-- Ubicación: database/seeds/leagues.sql
-- Responsabilidad: Capa DATABASE - Inserta las 5 ligas canónicas con api_id compatible con Football API y app/mocks/leagues.json.
-- Usa: tabla leagues (requiere DDL previo via init_db.sql o migraciones)
-- No hace: No crea torneos ni usuarios, solo catálogo de ligas.

INSERT INTO leagues (id, name, country, api_id) VALUES
    (39, 'Premier League', 'England', 39),
    (140, 'La Liga', 'Spain', 140),
    (135, 'Serie A', 'Italy', 135),
    (78, 'Bundesliga', 'Germany', 78),
    (61, 'Ligue 1', 'France', 61)
ON CONFLICT (id) DO NOTHING;

-- Verificación:
-- SELECT * FROM leagues ORDER BY id;
