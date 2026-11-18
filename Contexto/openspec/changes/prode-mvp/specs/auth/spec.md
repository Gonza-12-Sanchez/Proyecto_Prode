# Spec: auth

## Purpose

Gestiona el registro y autenticación de usuarios con validaciones estrictas y sesiones JWT de 24 horas para habilitar el acceso seguro a torneos y pronósticos.

## ADDED Requirements

### Requirement: User registration with validation

The system SHALL provide a registration form accepting email (max 254), username (3–30, alphanumeric plus `-`/`_`), and password (8–128 chars), validate email format and username pattern, enforce uniqueness of email/username, and create the account when valid.

#### Scenario: Successful registration

- **WHEN** a new user submits email `a@b.com`, username `user_1`, password `Secret123` (all valid and unique)
- **THEN** the system creates the account and returns success

#### Scenario: Duplicate email or username rejected

- **WHEN** a user submits registration with an email or username that already exists
- **THEN** the system returns an error indicating the specific conflict (email vs. username)

#### Scenario: Invalid email format rejected

- **WHEN** a user submits registration with email `not-an-email`
- **THEN** the system rejects with invalid email format error

#### Scenario: Invalid username pattern rejected

- **WHEN** a user submits username `ab` (too short) or `user@!` (invalid chars)
- **THEN** the system rejects with username validation error

#### Scenario: Password length enforced

- **WHEN** a user submits password of 7 chars or 129 chars
- **THEN** the system rejects with password length error (must be 8–128)

### Requirement: User authentication with JWT session

The system SHALL authenticate a registered user when credentials match stored email+password (bcrypt), return a session identifier (JWT) with 24h expiry, maintain access while session valid, and expire sessions after 24h inactivity; otherwise return authentication error.

#### Scenario: Successful login returns JWT

- **WHEN** a registered user provides correct email and password
- **THEN** the system authenticates and returns a JWT with `exp` 24h from now

#### Scenario: Invalid credentials rejected

- **WHEN** a user provides email/password that does not match any stored account
- **THEN** the system returns an authentication error message

#### Scenario: Session maintained while valid

- **GIVEN** a user with a valid JWT
- **WHEN** the user calls `GET /api/v1/users/me`
- **THEN** the system returns the profile (authenticated access maintained)

#### Scenario: Session expires after 24h

- **GIVEN** a JWT issued 25 hours ago
- **WHEN** the user makes an authenticated request
- **THEN** the system rejects with 401 expired session and requires re-login

