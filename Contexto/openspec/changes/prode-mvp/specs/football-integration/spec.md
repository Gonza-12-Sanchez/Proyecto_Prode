# Spec: football-integration

## Purpose

Sincroniza fixtures y resultados reales desde la Football API externa (con Adapter y Mock fallback) bajo tolerancia a fallos y condiciones de frescura estrictas para abastecer partidos jugables.

## ADDED Requirements

### Requirement: Match fixtures retrieval and display

The system SHALL retrieve match fixtures from Football_API for all 5 configured leagues every 24 hours, display team names, date, time, venue for each fixture, show only matches with start_time within next 7 days per tournament, exclude matches missing team names/date/time, and attempt up to 3 times with 5s intervals before showing unavailability.

#### Scenario: Fixtures refreshed every 24h for all leagues

- **WHEN** the fixtures_sync worker runs (cron 24h)
- **THEN** the system retrieves fixtures for Premier, La Liga, Serie A, Bundesliga, Ligue 1 and upserts into matches

#### Scenario: Display matches within next 7 days

- **WHEN** a user calls `GET /api/v1/tournaments/{id}/matches`
- **THEN** the system returns only matches where start_time is within next 7 days for that tournament's league

#### Scenario: Incomplete match data excluded

- **WHEN** Football API returns a match missing team names, date or time
- **THEN** the system excludes that match from display and does not store it

#### Scenario: Retry 3 times before unavailability message

- **GIVEN** Football API does not respond within 30s or returns HTTP error
- **WHEN** the Adapter makes the request
- **THEN** the system retries up to 3 times with 5s intervals and if still failing displays "match data is temporarily unavailable"

### Requirement: Match results propagation

The system SHALL when Football_API indicates Match status as finished retrieve final score within 10 minutes and update the Match result in all tournaments containing that Match within 1 minute.

#### Scenario: Result retrieved within 10min and propagated within 1min

- **GIVEN** a match with status finished in Football API and home 2-away 1
- **WHEN** the results_poller runs (every 10min)
- **THEN** the system retrieves the score within 10min and updates the matches table within 1 minute, triggering scoring

### Requirement: Adapter with Mock fallback

The system SHALL abstract Football API behind a `FootballPort` interface (`get_fixtures`, `get_results`) with an `ApiFootballAdapter` (httpx, timeout 30s, retry 3×/5s) and a `MockAdapter` serving `app/mocks/*.json` when `MOCK_MODE=true` or after 3 failures, logging `fallback_used=true`.

#### Scenario: Mock fallback when API unavailable

- **GIVEN** `MOCK_MODE=false` but API fails 3 times
- **WHEN** fixtures_sync runs
- **THEN** the system switches to MockAdapter, loads fixtures from JSON, and logs fallback_used

#### Scenario: Mock mode serves deterministic fixtures

- **GIVEN** `MOCK_MODE=true`
- **WHEN** fixtures_sync runs
- **THEN** the system loads 5 league mock files and upserts without external requests (0 cost)

