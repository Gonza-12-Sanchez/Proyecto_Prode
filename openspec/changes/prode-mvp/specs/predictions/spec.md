# Spec: predictions

## Purpose

Permite a participantes enviar y editar pronósticos de marcador exacto por partido con validaciones temporales estrictas y bloqueo permanente tras finalización para fair play.

## ADDED Requirements

### Requirement: Making predictions with temporal lock

The system SHALL display upcoming matches per tournament, allow participants to submit Prediction with home_score/away_score (≥0 integers), save when before match start_time, reject after start, allow editing until start, indicate whether a prediction has been submitted per match, and lock predictions permanently when result is finalized.

#### Scenario: Submit prediction before match start succeeds

- **GIVEN** a match with start_time in 2 hours and user is participant
- **WHEN** the user POSTs `{"home_score":2,"away_score":1}` to `/api/v1/matches/{id}/predictions`
- **THEN** the system saves the prediction and returns 201

#### Scenario: Prediction after start rejected

- **GIVEN** a match with start_time in the past
- **WHEN** the user attempts to submit or edit a prediction
- **THEN** the system rejects with error indicating match already started

#### Scenario: Edit prediction before start succeeds

- **GIVEN** a prediction exists for a future match
- **WHEN** the user PUTs `{"home_score":1,"away_score":1}` before start_time
- **THEN** the system updates the prediction

#### Scenario: Prediction locked after result finalized

- **GIVEN** a match with status FT and scored predictions
- **WHEN** a user attempts to edit that prediction
- **THEN** the system rejects and the prediction remains locked permanently

#### Scenario: Display whether prediction submitted

- **WHEN** a user views matches in a tournament
- **THEN** each match indicates whether the user has submitted a prediction (boolean/submitted flag)

