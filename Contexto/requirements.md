# Requirements Document

## Introduction

Este documento define los requisitos para una aplicación móvil de torneos de pronósticos de fútbol. La aplicación permite a los usuarios crear torneos privados o unirse a torneos existentes para hacer pronósticos sobre partidos reales de múltiples ligas de fútbol. El sistema incluye autenticación de usuarios, configuración flexible de torneos, modelo de monetización freemium con publicidad, funcionalidades sociales, y notificaciones en tiempo real.

## Glossary

- **System**: La aplicación móvil de torneos de pronósticos de fútbol completa
- **User**: Cualquier persona registrada en la aplicación
- **Tournament_Creator**: Usuario que crea y configura un torneo
- **Tournament_Participant**: Usuario que se une a un torneo existente
- **Tournament**: Competencia privada donde usuarios hacen pronósticos sobre partidos de fútbol
- **Prediction**: Pronóstico de un usuario sobre el resultado de un partido específico
- **Match**: Partido de fútbol real con equipos, fecha, y resultado
- **League**: Competencia oficial de fútbol (ej: Premier League, La Liga)
- **Scoring_System**: Sistema de puntos configurado por el Tournament_Creator
- **Free_User**: Usuario con acceso a funcionalidades básicas
- **Premium_User**: Usuario con suscripción que accede a funcionalidades avanzadas
- **Football_API**: Servicio externo que proporciona datos de partidos y resultados en tiempo real
- **Profile**: Información personal y estadísticas de un User
- **Notification**: Alerta enviada al usuario sobre eventos relevantes
- **Chat**: Sistema de mensajería entre Tournament_Participants
- **Leaderboard**: Tabla de posiciones que muestra el ranking de participantes en un Tournament

## Requirements

### Requirement 1: User Authentication and Registration

**User Story:** As a new user, I want to create an account and log in, so that I can access the application and participate in tournaments.

#### Acceptance Criteria

1. THE System SHALL provide a registration form that accepts email (maximum 254 characters), username (3 to 30 characters), and password
2. WHEN a User submits registration data, THE System SHALL validate that the email address conforms to standard email format
3. WHEN a User submits registration data, THE System SHALL validate that the username contains only alphanumeric characters, hyphens, and underscores
4. WHEN a User submits valid registration data with a unique email and username, THE System SHALL create a new user account
5. IF a User submits registration data with an email or username that already exists, THEN THE System SHALL return an error message indicating the specific conflict
6. THE System SHALL require passwords to be between 8 and 128 characters in length
7. WHEN a registered User provides credentials matching a stored email and password, THE System SHALL authenticate the User and return a session identifier
8. IF a User provides credentials that do not match any stored account, THEN THE System SHALL return an authentication error message
9. WHILE a User has a valid session identifier, THE System SHALL maintain authenticated access to the application
10. THE System SHALL expire User sessions after 24 hours of inactivity

### Requirement 2: User Profile Management

**User Story:** As a User, I want to manage my profile and view my statistics, so that I can track my performance and personalize my account.

#### Acceptance Criteria

1. WHEN a User accesses their Profile page, THE System SHALL display username, email, favorite teams, tournaments played count, current streak, and statistics
2. WHEN a User updates their email, THE System SHALL save the change
3. IF a User submits an invalid email format, THEN THE System SHALL reject the update and display an error message indicating invalid email format
4. WHEN a User selects favorite teams, THE System SHALL allow selection of up to 10 teams from available leagues
5. WHEN a User accesses their Profile page, THE System SHALL display their current prediction streak as the count of consecutive correct predictions since the last incorrect prediction or zero if no predictions exist
6. WHEN a User makes an incorrect prediction, THE System SHALL reset their current prediction streak to zero
7. WHEN a User accesses their Profile page, THE System SHALL display the total count of tournaments in which the User has made at least one prediction
8. WHEN a User accesses their Profile page, THE System SHALL display total predictions made, accuracy percentage rounded to one decimal place, and best tournament finish as highest ranking position achieved

### Requirement 3: Tournament Creation

**User Story:** As a Tournament_Creator, I want to create a new tournament with custom rules, so that I can organize a prediction competition with my friends.

#### Acceptance Criteria

1. WHEN a User initiates tournament creation, THE System SHALL display a tournament configuration form
2. THE System SHALL allow the Tournament_Creator to select a League from available options
3. THE System SHALL allow the Tournament_Creator to configure a Scoring_System including points for exact score, correct winner, and goal difference
4. WHEN a Free_User creates a Tournament, THE System SHALL limit the maximum number of participants to 10
5. WHEN a Premium_User creates a Tournament, THE System SHALL allow up to 100 participants
6. THE System SHALL allow the Tournament_Creator to set a tournament name and description
7. WHEN the Tournament_Creator saves a valid tournament configuration, THE System SHALL create the Tournament and assign the creator as the first participant

### Requirement 4: Tournament Discovery and Joining

**User Story:** As a User, I want to find and join existing tournaments, so that I can participate in prediction competitions.

#### Acceptance Criteria

1. THE System SHALL allow Tournament_Creators to generate a unique invitation code consisting of 8 alphanumeric characters that is unique across all active Tournaments
2. WHEN a User enters a valid invitation code, THE System SHALL display tournament details including name, league, scoring rules, current participant count, and maximum capacity within 2 seconds
3. IF a User enters an invitation code that does not match any active Tournament, THEN THE System SHALL display an error message indicating the code is invalid
4. WHEN a User confirms joining a Tournament with fewer participants than maximum capacity of 50, THE System SHALL add the User as a Tournament_Participant
5. IF a User attempts to join a Tournament that has reached maximum capacity of 50 participants, THEN THE System SHALL display an error message indicating the Tournament is full and prevent the join action
6. IF a User attempts to join a Tournament they have already joined, THEN THE System SHALL display an error message indicating they are already a participant and prevent the duplicate join
7. WHEN a User requests to view their tournaments, THE System SHALL display a list of all Tournaments the User has joined

### Requirement 5: Football Match Data Integration

**User Story:** As a User, I want to see real football matches and results, so that I can make informed predictions.

#### Acceptance Criteria

1. THE System SHALL retrieve match fixtures from the Football_API for all configured leagues every 24 hours
2. THE System SHALL display match information including team names, match date, match time, and venue for each retrieved fixture
3. WHEN the Football_API indicates a Match status as finished, THE System SHALL retrieve the final score within 10 minutes
4. WHEN a final score is retrieved from the Football_API, THE System SHALL update the Match result in all tournaments containing that Match within 1 minute
5. THE System SHALL display all matches with scheduled start times within the next 7 days for each Tournament
6. IF the Football_API does not respond within 30 seconds or returns an HTTP error status, THEN THE System SHALL display a message indicating that match data is temporarily unavailable
7. IF the Football_API returns incomplete match data missing any of team names, match date, or match time, THEN THE System SHALL exclude that match from display
8. THE System SHALL attempt to retrieve data from the Football_API up to 3 times with 5 second intervals between attempts before displaying an unavailability message

### Requirement 6: Making Predictions

**User Story:** As a Tournament_Participant, I want to submit predictions for upcoming matches, so that I can compete for points in the tournament.

#### Acceptance Criteria

1. THE System SHALL display all upcoming matches in each Tournament the User participates in
2. THE System SHALL allow Tournament_Participants to submit a Prediction with home team score and away team score
3. WHEN a Tournament_Participant submits a Prediction before the match start time, THE System SHALL save the Prediction
4. WHEN a Tournament_Participant attempts to submit a Prediction after the match has started, THE System SHALL reject the Prediction
5. THE System SHALL allow Tournament_Participants to edit their Predictions until the match starts
6. THE System SHALL display whether a Prediction has been submitted for each upcoming Match
7. WHEN a Match result is finalized, THE System SHALL lock the corresponding Predictions permanently

### Requirement 7: Scoring and Points Calculation

**User Story:** As a Tournament_Participant, I want my predictions to be scored accurately, so that I can see my ranking in the tournament.

#### Acceptance Criteria

1. WHEN a Match result is finalized, THE System SHALL calculate points for all Predictions associated with that Match based on the Tournament's Scoring_System
2. WHEN calculating points for a Prediction, THE System SHALL compare the Prediction's home_score and away_score against the Match's final home_score and away_score
3. WHEN a Prediction's home_score and away_score exactly match the Match's final home_score and away_score, THE System SHALL award the exact_match points defined in the Scoring_System
4. WHEN a Prediction correctly identifies the winning team but does not exactly match the scores, THE System SHALL award the correct_winner points defined in the Scoring_System
5. WHEN a Prediction correctly identifies the goal difference but does not exactly match the scores, THE System SHALL award the correct_difference points defined in the Scoring_System
6. WHEN multiple scoring criteria are satisfied for a Prediction, THE System SHALL award points cumulatively for all satisfied criteria
7. WHEN a Prediction satisfies no scoring criteria, THE System SHALL award zero points for that Prediction
8. WHEN points are calculated for a Prediction, THE System SHALL add the calculated points to the Tournament_Participant's total score for that Tournament
9. WHEN all Predictions for a Match have been scored, THE System SHALL recalculate the Tournament Leaderboard rankings
10. WHEN a Prediction has been scored, THE System SHALL display the earned points for that Prediction to the Tournament_Participant

### Requirement 8: Tournament Leaderboard

**User Story:** As a Tournament_Participant, I want to view the tournament rankings, so that I can see how I compare to other participants.

#### Acceptance Criteria

1. THE System SHALL display a Leaderboard for each Tournament showing participant rankings
2. THE System SHALL order the Leaderboard by total points in descending order
3. WHEN multiple participants have the same points, THE System SHALL rank them by accuracy percentage
4. THE System SHALL display each participant's username, total points, predictions made, and accuracy percentage
5. THE System SHALL highlight the current User's position in the Leaderboard
6. THE System SHALL update the Leaderboard within 5 minutes after Match results are scored

### Requirement 9: Free Tier Features

**User Story:** As a Free_User, I want to access basic tournament features, so that I can try the application before deciding to upgrade.

#### Acceptance Criteria

1. THE System SHALL allow Free_Users to create tournaments with basic Scoring_System configurations
2. THE System SHALL limit Free_Users to maximum 10 participants per Tournament
3. THE System SHALL allow Free_Users to join unlimited tournaments as Tournament_Participant
4. THE System SHALL allow Free_Users to make Predictions on all matches in their tournaments
5. THE System SHALL allow Free_Users to view Leaderboards and Profile statistics
6. THE System SHALL display advertisements to Free_Users every 5 interactions

### Requirement 10: Premium Subscription

**User Story:** As a User, I want to subscribe to premium features, so that I can create larger tournaments and access advanced features.

#### Acceptance Criteria

1. THE System SHALL provide a subscription interface for upgrading to Premium_User status
2. WHEN a User completes premium subscription payment, THE System SHALL upgrade the User to Premium_User
3. THE System SHALL allow Premium_Users to create tournaments with up to 100 participants
4. THE System SHALL allow Premium_Users to configure advanced Scoring_System rules
5. THE System SHALL remove advertisements for Premium_Users
6. THE System SHALL maintain Premium_User status while the subscription is active
7. WHEN a premium subscription expires, THE System SHALL revert the User to Free_User status

### Requirement 11: Advertisement Integration

**User Story:** As the application owner, I want to display advertisements to free users, so that I can generate revenue.

#### Acceptance Criteria

1. THE System SHALL integrate with an advertisement platform
2. WHEN a Free_User completes 5 interactions, THE System SHALL display an advertisement
3. THE System SHALL NOT display advertisements to Premium_Users
4. THE System SHALL count page views, predictions submitted, and leaderboard refreshes as interactions
5. THE System SHALL reset the interaction counter after displaying an advertisement
6. WHEN the advertisement platform is unavailable, THE System SHALL continue normal operation without ads

### Requirement 12: Tournament Chat

**User Story:** As a Tournament_Participant, I want to chat with other participants, so that I can discuss predictions and engage with the community.

#### Acceptance Criteria

1. THE System SHALL provide a Chat interface for each Tournament
2. WHEN a Tournament_Participant sends a message, THE System SHALL broadcast it to all participants in that Tournament
3. THE System SHALL display Chat messages with sender username and timestamp
4. THE System SHALL order Chat messages chronologically
5. THE System SHALL limit Chat messages to 500 characters
6. THE System SHALL load the most recent 50 Chat messages when opening the Chat interface
7. WHEN a new Chat message is received, THE System SHALL notify Tournament_Participants who have the Chat open

### Requirement 13: Push Notifications

**User Story:** As a Tournament_Participant, I want to receive notifications about important events, so that I don't miss predictions or updates.

#### Acceptance Criteria

1. IF a User has not submitted a Prediction for a Match AND the Match starts within 2 hours, THEN THE System SHALL send a Notification to that User indicating the Match details and time remaining
2. WHEN Match results are available and scored, THE System SHALL send a Notification to Users who submitted Predictions for that Match indicating the Match outcome and Points earned
3. WHEN a User's Leaderboard position changes by 3 or more ranks, THE System SHALL send a Notification to that User indicating the new position and rank change
4. WHEN a User receives a Tournament invitation, THE System SHALL send a Notification to that User indicating the Tournament name and inviter
5. THE System SHALL allow Users to enable or disable Notifications in their Profile settings
6. IF a User has Notifications disabled, THEN THE System SHALL NOT send any Notifications to that User
7. THE System SHALL send Notifications through the mobile platform's push notification service
8. IF a Notification fails to deliver, THEN THE System SHALL retry delivery up to 3 times with exponential backoff intervals of 1 minute, 5 minutes, and 15 minutes
9. IF a Match start time is unavailable or changes after a reminder Notification has been scheduled, THEN THE System SHALL cancel the scheduled Notification for that Match

### Requirement 14: Social Sharing

**User Story:** As a Tournament_Participant, I want to share my achievements on social media, so that I can celebrate with friends.

#### Acceptance Criteria

1. THE System SHALL provide a share button on the Profile page
2. THE System SHALL provide a share button on the Leaderboard when the User is in the top 3
3. WHEN a User activates sharing, THE System SHALL generate a shareable message with User statistics
4. THE System SHALL allow sharing to Facebook, Twitter, Instagram, and WhatsApp
5. THE System SHALL include the Tournament invitation code in shared messages about specific tournaments
6. THE System SHALL generate shareable images showing Leaderboard position and key statistics

### Requirement 15: Tournament Invitation Management

**User Story:** As a Tournament_Creator, I want to invite specific people to my tournament, so that I can build my competition community.

#### Acceptance Criteria

1. THE System SHALL allow the Tournament_Creator to generate shareable invitation links
2. THE System SHALL allow the Tournament_Creator to copy the Tournament invitation code
3. WHEN an invited User opens an invitation link, THE System SHALL display the Tournament details
4. THE System SHALL allow the Tournament_Creator to view a list of all Tournament_Participants
5. THE System SHALL allow the Tournament_Creator to remove participants from the Tournament before it starts
6. WHEN the Tournament has started, THE System SHALL prevent the Tournament_Creator from removing participants

### Requirement 16: Multi-League Support

**User Story:** As a Tournament_Creator, I want to select from multiple football leagues, so that I can create tournaments for different competitions.

#### Acceptance Criteria

1. THE System SHALL retrieve available leagues from the Football_API
2. THE System SHALL display a list of supported leagues including Premier League, La Liga, Serie A, Bundesliga, and Ligue 1
3. WHEN a Tournament_Creator selects a League, THE System SHALL configure the Tournament to include matches from only that League
4. THE System SHALL display league name and logo in Tournament details
5. THE System SHALL allow Free_Users to select from all available leagues

### Requirement 17: Prediction History

**User Story:** As a Tournament_Participant, I want to view my past predictions and results, so that I can learn from my performance.

#### Acceptance Criteria

1. THE System SHALL display a history of all Predictions made by the User in each Tournament
2. THE System SHALL show each Prediction with the predicted score, actual score, and points earned
3. THE System SHALL order Prediction history chronologically with most recent first
4. THE System SHALL allow filtering Prediction history by Tournament
5. THE System SHALL display accuracy statistics for completed predictions
6. THE System SHALL indicate which Predictions are still pending Match results

### Requirement 18: Streak Tracking

**User Story:** As a User, I want to track my prediction streaks, so that I can challenge myself to maintain consistency.

#### Acceptance Criteria

1. THE System SHALL calculate the User's current winning streak across all tournaments
2. THE System SHALL increment the streak counter when a Prediction earns any points
3. WHEN a Prediction earns zero points, THE System SHALL reset the streak counter to zero
4. THE System SHALL display the current streak on the User Profile
5. THE System SHALL track and display the User's longest historical streak
6. THE System SHALL consider only completed and scored predictions for streak calculation

### Requirement 19: Tournament Status Management

**User Story:** As a Tournament_Creator, I want to control when my tournament starts, so that I can ensure all participants are ready.

#### Acceptance Criteria

1. WHEN a Tournament is created, THE System SHALL set the status to "Setup"
2. WHILE a Tournament status is "Setup", THE System SHALL allow the Tournament_Creator to modify scoring rules and participant limit
3. THE System SHALL allow the Tournament_Creator to manually start the Tournament
4. WHEN a Tournament is started, THE System SHALL change the status to "Active" and lock configuration changes
5. WHEN all matches in a Tournament are completed and scored, THE System SHALL change the status to "Completed"
6. THE System SHALL display Tournament status on the Tournament details page

### Requirement 20: Data Persistence and Synchronization

**User Story:** As a User, I want my data to be saved and synchronized, so that I can access it from any device.

#### Acceptance Criteria

1. THE System SHALL store all User data, Predictions, and Tournament information in a backend database
2. WHEN a User makes a Prediction, THE System SHALL save it to the database within 2 seconds
3. WHEN the mobile device loses network connectivity, THE System SHALL queue data changes locally
4. WHEN network connectivity is restored, THE System SHALL synchronize queued changes with the backend
5. THE System SHALL prevent data loss during synchronization conflicts by preserving the server version for scored data
6. THE System SHALL display a synchronization status indicator when data is being synced
7. WHEN a User logs in from a different device, THE System SHALL load the most recent data from the backend

