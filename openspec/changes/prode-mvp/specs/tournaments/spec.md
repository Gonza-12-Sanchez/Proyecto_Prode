# Spec: tournaments

## Purpose

Permite crear torneos privados con liga y scoring configurables, unirse vía código de 8 caracteres, gestionar invitaciones y estados del ciclo de vida con límites Free/Premium.

## ADDED Requirements

### Requirement: Tournament creation with league and scoring

The system SHALL display a configuration form allowing selection of 1 league from 5 (Premier, La Liga, Serie A, Bundesliga, Ligue 1), configuration of Scoring_System (exact_score, correct_winner, goal_difference), name/description, and enforce Free max 10 / Premium max 50 participants; on save it SHALL create the tournament, assign creator as first participant, and set status to Setup.

#### Scenario: Free user creates tournament with 10 max

- **WHEN** a Free user POSTs `{"name":"Amigos","league_id":39,"scoring_rules":{"exact_score":5,"correct_winner":3,"goal_difference":2}}`
- **THEN** the system creates the tournament with max_participants=10, scoring_rules stored, creator as participant, status Setup

#### Scenario: Premium user creates tournament with 50 max

- **WHEN** a Premium user POSTs a tournament requesting 50 participants
- **THEN** the system allows up to 50 and creates it

#### Scenario: Reject exceeding limit for tier

- **WHEN** a Free user attempts max_participants=50 or Premium requests 51
- **THEN** the system rejects with tier limit error

### Requirement: Tournament discovery and joining by invite code

The system SHALL generate a unique 8-char alphanumeric invite_code per active tournament, display details (name, league, scoring rules, occupancy) within 2 seconds when a valid code is entered, allow joining when below max capacity 50, and reject invalid code, full tournament, or duplicate membership with specific errors; it SHALL also list all tournaments the user has joined.

#### Scenario: Join with valid code previews within 2s

- **WHEN** a user enters a valid invite_code `A1B2C3D4`
- **THEN** the system returns tournament details within 2 seconds

#### Scenario: Invalid code rejected

- **WHEN** a user enters `ZZZZZZZZ` not matching any active tournament
- **THEN** the system displays error indicating code is invalid

#### Scenario: Join succeeds when not full

- **GIVEN** a tournament with 10/50 participants and user not yet member
- **WHEN** the user confirms joining
- **THEN** the system adds the user as participant

#### Scenario: Join rejected when full

- **GIVEN** a tournament with 50/50 participants
- **WHEN** a new user attempts to join
- **THEN** the system displays error indicating tournament is full and prevents join

#### Scenario: Duplicate join rejected

- **GIVEN** a user already participant in tournament `A1B2C3D4`
- **WHEN** the same user attempts to join again
- **THEN** the system displays error indicating already a participant

#### Scenario: List my tournaments

- **WHEN** a user requests `GET /api/v1/tournaments`
- **THEN** the system returns all tournaments the user participates in

### Requirement: Tournament invitation management

The system SHALL allow generating shareable invitation links, copying invite_code, viewing participant list, and removing participants only while status is Setup (prevent removal once Active).

#### Scenario: Creator copies invite code

- **WHEN** the creator requests the tournament invite code
- **THEN** the system returns the 8-char code for sharing

#### Scenario: Creator removes participant in Setup

- **GIVEN** tournament status is Setup
- **WHEN** the creator removes a participant
- **THEN** the system removes that participant

#### Scenario: Removal blocked in Active

- **GIVEN** tournament status is Active
- **WHEN** the creator attempts to remove a participant
- **THEN** the system prevents removal and returns error indicating tournament already started

### Requirement: Multi-league support

The system SHALL support 5 leagues (Premier League, La Liga, Serie A, Bundesliga, Ligue 1) retrieved from Football API or seeded, display name/logo, configure tournament to include matches from only the selected league, and allow Free users to select any league.

#### Scenario: Create tournament with La Liga

- **WHEN** a user selects league `140` (La Liga)
- **THEN** the system configures the tournament to include only La Liga matches and displays league name/logo in details

#### Scenario: Free user selects any league

- **WHEN** a Free user selects Serie A
- **THEN** the system allows it (no tier restriction on league choice)

### Requirement: Tournament status management

The system SHALL set status to Setup on creation, allow editing scoring rules/participant limit only in Setup, allow creator to manually start (Setup→Active, locking config), auto-transition to Completed when all matches finished and scored, and display status on details page.

#### Scenario: Setup allows editing config

- **GIVEN** tournament status Setup
- **WHEN** the creator PATCHes scoring_rules
- **THEN** the system allows the update

#### Scenario: Start locks configuration

- **WHEN** the creator POSTs `/tournaments/{id}/start`
- **THEN** the system changes status to Active and rejects further config edits

#### Scenario: Completed when all matches scored

- **GIVEN** a tournament where all matches have status FT and all predictions scored
- **WHEN** the last match is scored
- **THEN** the system sets status to Completed

