@echo off
setlocal disabledelayedexpansion
cd /d "%~dp0"

if not exist ".env" (
  echo [FAIL] .env not found. Run this file from your capstone-project folder.
  pause
  exit /b 1
)

REM Load values from .env (lines starting with # are skipped)
for /f "usebackq eol=# tokens=1,* delims==" %%a in (".env") do set "%%a=%%b"

set PASS=0
set FAIL=0

echo.
echo ===== CAPSTONE SMOKE TEST =====
echo.
echo --- 1. Containers running ---
for %%s in (db keycloak backend minio) do call :svc %%s

echo.
echo --- 2. Two databases on one server ---
call :q %DB_NAME% "SELECT 1 FROM pg_database WHERE datname='%DB_NAME%'"
if "%R%"=="1" (call :ok "App database exists") else (call :fail "App database missing")
call :q %DB_NAME% "SELECT 1 FROM pg_database WHERE datname='%KC_DB_NAME%'"
if "%R%"=="1" (call :ok "Keycloak database exists") else (call :fail "Keycloak database missing - check KC_DB_NAME in .env")

echo.
echo --- 3. Schema and tables ---
call :q %DB_NAME% "SELECT 1 FROM information_schema.schemata WHERE schema_name='capstone'"
if "%R%"=="1" (call :ok "Schema capstone exists") else (call :fail "Schema capstone missing")
call :q %DB_NAME% "SELECT 1 FROM information_schema.tables WHERE table_schema='capstone' AND table_name='candidates'"
if "%R%"=="1" (call :ok "capstone.candidates exists") else (call :fail "capstone.candidates missing")
call :q %DB_NAME% "SELECT 1 FROM information_schema.tables WHERE table_schema='capstone' AND table_name='candidate_user_mapping'"
if "%R%"=="1" (call :ok "capstone.candidate_user_mapping exists") else (call :fail "capstone.candidate_user_mapping missing")
call :q %DB_NAME% "SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='candidates'"
if "%R%"=="1" (call :fail "Old candidates table still in public schema") else (call :ok "No stray tables in public schema")
docker compose exec -T db psql -U %DB_USER% -d %DB_NAME% -tAc "SHOW search_path" | findstr /b "capstone" >nul
if errorlevel 1 (call :fail "search_path does not start with capstone - run the ALTER ROLE command") else (call :ok "search_path starts with capstone")

echo.
echo --- 4. Keycloak is using its own database ---
call :q %KC_DB_NAME% "SELECT 1 FROM information_schema.tables WHERE table_name='realm' LIMIT 1"
if "%R%"=="1" (call :ok "Keycloak tables exist in the keycloak database") else (call :fail "No Keycloak tables yet - Keycloak is not connected to the DB")

echo.
echo --- 5. Web endpoints ---
call :http "Keycloak realm %KC_REALM%" "http://localhost:8080/realms/%KC_REALM%"
call :http "Keycloak JWKS keys" "http://localhost:8080/realms/%KC_REALM%/protocol/openid-connect/certs"
call :http "Backend /docs" "http://localhost:8002/docs"
call :http "MinIO console" "http://localhost:9001"

echo.
echo --- 6. Backend log errors ---
docker compose logs backend --tail 200 | findstr /i /c:"does not exist" /c:"Traceback" /c:"authentication failed" >nul
if errorlevel 1 (call :ok "No DB or traceback errors in backend logs") else (call :fail "Errors found - run: docker compose logs backend --tail 50")

echo.
echo ===== RESULT: %PASS% passed, %FAIL% failed =====
if %FAIL% GTR 0 (
  echo Copy everything above and paste it to Claude to see what to fix.
) else (
  echo All good. Now test /report-0 and /report-final by hand in the app.
)
echo.
pause
exit /b 0

:svc
docker compose ps --status running --services | findstr /x "%~1" >nul
if errorlevel 1 (call :fail "%~1 container running") else (call :ok "%~1 container running")
exit /b

:q
set "R="
for /f "usebackq delims=" %%i in (`docker compose exec -T db psql -U %DB_USER% -d %~1 -tAc "%~2" 2^>nul`) do set "R=%%i"
exit /b

:http
set "C=000"
for /f %%i in ('curl -s -o NUL -w "%%{http_code}" %~2') do set "C=%%i"
if "%C%"=="200" (call :ok "%~1 (HTTP 200)") else (call :fail "%~1 returned HTTP %C%")
exit /b

:ok
set /a PASS+=1
echo [PASS] %~1
exit /b

:fail
set /a FAIL+=1
echo [FAIL] %~1
exit /b
