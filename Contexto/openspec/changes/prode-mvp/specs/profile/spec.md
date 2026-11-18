# Spec: profile

## Purpose

Permite al usuario gestionar su perfil, favoritos y visualizar estadísticas derivadas (racha, accuracy, torneos jugados) para seguimiento de rendimiento personal.

## ADDED Requirements

### Requirement: Profile display

The system SHALL display on the Profile page: username, email, favorite teams, tournaments played count (distinct tournaments with ≥1 prediction), current streak, total predictions, accuracy % (1 decimal), and best tournament finish.

#### Scenario: Profile shows all fields

- **WHEN** a user accesses `GET /api/v1/users/me`
- **THEN** the system returns username, email, favorite_teams (≤10), tournaments_played, current_streak, total_predictions, accuracy (e.g. 66.7%), best_finish

### Requirement: Profile email update with validation

The system SHALL save an email change when format is valid; otherwise reject with invalid email format error.

#### Scenario: Valid email update succeeds

- **WHEN** a user PATCHes email to `new@valid.com` with valid format
- **THEN** the system saves the change and returns updated profile

#### Scenario: Invalid email update rejected

- **WHEN** a user PATCHes email to `bad-email`
- **THEN** the system rejects with invalid email format error and does not persist

### Requirement: Favorite teams selection

The system SHALL allow selection of up to 10 favorite teams from available leagues and persist the selection.

#### Scenario: Select up to 10 favorites

- **WHEN** a user selects 3 teams and PATCHes profile
- **THEN** the system saves the 3 teams and displays them on next GET

#### Scenario: Exceeding 10 favorites rejected

- **WHEN** a user attempts to select 11 teams
- **THEN** the system rejects with limit exceeded error

### Requirement: Streak calculation (profile)

The system SHALL calculate current streak as count of consecutive correct predictions (each with >0 points) since last incorrect (0 pts) or 0 if none; reset to 0 on an incorrect prediction; display total tournaments with ≥1 prediction, total predictions, accuracy rounded to 1 decimal, and best finish.

#### Scenario: Streak increments on correct prediction

- **GIVEN** a user with current_streak 2
- **WHEN** the next prediction earns >0 points
- **THEN** the system increments current_streak to 3

#### Scenario: Streak resets on incorrect prediction

- **WHEN** a user makes a prediction that earns 0 points
- **THEN** the system resets current_streak to 0

#### Scenario: Accuracy calculation

- **WHEN** a user has 4 predictions, 3 earned >0 pts
- **THEN** the system displays accuracy 75.0% (3/4, 1 decimal)

