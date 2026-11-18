# Spec: scoring

## Purpose

Calcula puntos acumulativos por pronóstico, mantiene leaderboard ordenado con desempate por accuracy, historial filtrable y rachas para ranking competitivo y motivación.

## ADDED Requirements

### Requirement: Scoring and points calculation (accumulative)

The system SHALL when a match result is finalized calculate points for all predictions of that match based on tournament's Scoring_System by comparing predicted vs actual scores; award exact_match points if exact, correct_winner if same winner (not exact), correct_difference if same goal difference (not exact); award cumulatively if multiple criteria satisfied; award 0 if none; add points to participant's total for that tournament; recalculate leaderboard; display earned points per prediction.

#### Scenario: Exact score awards all applicable points cumulatively

- **GIVEN** scoring_rules `exact_score=5, correct_winner=3, goal_difference=2`, prediction 2-1 vs actual 2-1
- **WHEN** the match is scored
- **THEN** the system awards 5+3+2=10 points (exact implies winner and diff) and adds 10 to total_points

#### Scenario: Correct winner only

- **GIVEN** same rules, prediction 1-0 vs actual 2-1 (same winner, different diff)
- **WHEN** scored
- **THEN** the system awards 3 points (correct_winner only)

#### Scenario: Correct goal difference only

- **GIVEN** prediction 0-0 vs actual 1-1 (both draws, diff 0, but different scores)
- **WHEN** scored
- **THEN** the system awards goal_difference (2) and if draw counts as correct_winner per rules, awards cumulatively as defined

#### Scenario: No criteria awards zero

- **GIVEN** prediction 0-2 vs actual 3-0
- **WHEN** scored
- **THEN** the system awards 0 points

#### Scenario: Points added and leaderboard recalculated

- **WHEN** points are calculated for a prediction
- **THEN** the system adds them to `tournament_participants.total_points` for that tournament and recalculates leaderboard rankings

#### Scenario: Earned points displayed

- **WHEN** a prediction has been scored
- **THEN** `GET /users/me/predictions` shows `points_earned` for that prediction

### Requirement: Tournament leaderboard

The system SHALL display per tournament a leaderboard ordered by total_points DESC, tie-break by accuracy %, showing username, total_points, predictions made, accuracy %, highlighting current user's position, and updating within 5 minutes after scoring.

#### Scenario: Leaderboard ordered with tie-break

- **GIVEN** users A 20 pts 80% acc, B 20 pts 60% acc, C 15 pts
- **WHEN** leaderboard is requested
- **THEN** the order is A, B, C (B after A by accuracy tie-break)

#### Scenario: Leaderboard highlights current user

- **WHEN** the authenticated user requests the leaderboard
- **THEN** the response marks `is_current_user: true` on their row

#### Scenario: Leaderboard updates within 5 min after scoring

- **WHEN** a match is scored
- **THEN** the system recalculates and the next GET within 5 minutes reflects new rankings

### Requirement: Prediction history

The system SHALL display history of all predictions per tournament with predicted vs actual vs points, ordered most recent first, filterable by tournament, indicating pending vs scored, and showing accuracy for completed predictions.

#### Scenario: History ordered and shows pending

- **WHEN** a user GETs `/api/v1/users/me/predictions`
- **THEN** the system returns predictions ordered by match start_time desc, each with `predicted(2-1), actual(null if pending), points_earned(null if pending)`, pending flag true if not yet scored

#### Scenario: Filter history by tournament

- **WHEN** a user GETs `/users/me/predictions?tournament_id=X`
- **THEN** the system returns only predictions for tournament X

### Requirement: Streak tracking

The system SHALL calculate current winning streak across all tournaments (consecutive scored predictions with >0 pts), increment on any points >0, reset to 0 on 0 pts, display current and longest historical streak on profile, considering only completed/scored predictions.

#### Scenario: Streak increments on scoring with points

- **GIVEN** current_streak 1 and a new prediction scores 3 pts
- **WHEN** scored
- **THEN** the system increments current_streak to 2 and updates longest if greater

#### Scenario: Streak resets on zero points

- **WHEN** a scored prediction earns 0 points
- **THEN** the system resets current_streak to 0

#### Scenario: Only scored predictions count

- **GIVEN** a pending prediction exists
- **WHEN** streak is calculated
- **THEN** the system excludes pending predictions from count

