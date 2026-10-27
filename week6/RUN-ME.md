# Run the capstone with Docker Compose

All commands in PowerShell, inside the project folder (the one with the Dockerfile).

1. Stop old containers (this does NOT delete them):
   docker stop $(docker ps -q)

2. Start everything:
   docker compose up -d --build

3. Wait about 60 seconds (Keycloak is slow), then check:
   docker compose ps

4. Get the candidate's id (for candidate_user_id):
   powershell -ExecutionPolicy Bypass -File .\show-candidate-id.ps1

5. Get an admin token (paste into Swagger > Authorize, without the word Bearer):
   powershell -ExecutionPolicy Bypass -File .\get-token.ps1

6. Candidate token (for /report-final):
   powershell -ExecutionPolicy Bypass -File .\get-token.ps1 -User candidate1 -Pass 'Candidate@12345'

7. Swagger: http://localhost:8002/docs
   Keycloak console: http://localhost:8080  (admin / KcAdmin2026)

Stop (keeps data):        docker compose down
Stop and wipe all data:   docker compose down -v
Logs of the API:          docker compose logs -f backend

Test users: admin1 / Admin@12345 (role admin), candidate1 / Candidate@12345 (role user)
