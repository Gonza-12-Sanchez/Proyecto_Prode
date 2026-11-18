# Spec: persistence

## Purpose

Garantiza persistencia transaccional en PostgreSQL y sincronización resiliente con cola offline, idempotencia y resolución server-wins para datos ya scoreados.

## ADDED Requirements

### Requirement: Data persistence and synchronization

The system SHALL store all user data, predictions and tournament info in PostgreSQL, save a prediction within 2 seconds, queue changes locally when offline, synchronize queued changes on reconnect, preserve server version for scored data on conflicts (server-wins), display sync status indicator during sync, and load most recent backend data when logging in from another device.

#### Scenario: Save prediction within 2 seconds

- **WHEN** a user POSTs a prediction while online
- **THEN** the system persists to PostgreSQL and returns success within 2 seconds

#### Scenario: Offline queue and sync on reconnect

- **GIVEN** device offline and user creates a prediction for a future match
- **WHEN** the device was offline the prediction is queued locally as `{op:"create", payload, ts}`
- **THEN** on reconnect the system synchronizes queued changes in ts order via `POST /predictions` and returns success

#### Scenario: Server-wins for scored data conflicts

- **GIVEN** a prediction already scored with `points_earned=5` on server and a queued offline edit for same match tries to overwrite to 3-0
- **WHEN** sync runs
- **THEN** the system preserves server version (points_earned NOT NULL → server-wins) and rejects the stale overwrite

#### Scenario: Pending conflict uses last-write-wins

- **GIVEN** a prediction still pending (points_earned IS NULL) with local edit vs server edit
- **WHEN** sync runs
- **THEN** the system resolves by `updated_at` last-write-wins (latest timestamp prevails)

#### Scenario: Sync status indicator

- **WHEN** synchronization is in progress
- **THEN** the system exposes `X-Sync-Status: syncing` header or `GET /sync/status` indicating syncing state to display indicator

#### Scenario: Multi-device loads most recent backend data

- **WHEN** a user logs in from a different device
- **THEN** the system loads the most recent predictions/tournaments from backend (canonical store)

