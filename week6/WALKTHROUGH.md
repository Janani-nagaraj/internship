# Walkthrough: Document Verification API

## What I built
A backend that verifies two scanned documents for a candidate. An admin uploads a degree certificate and a marksheet. The candidate, logged in with their own account, asks for the final report. The service reads both images with Tesseract OCR, compares the name and register number, and returns a three-page PDF with the result. I also added a Candidates resource with full CRUD (create, list, read, update, delete) for admins.

## How it is wired
- **FastAPI** is the backend. The code is organised into folders by job: `core` (settings and security), `db` (PostgreSQL code), `schemas` (Pydantic data shapes), `services` (storage, OCR, verification, PDF, validation) and `routes` (the HTTP endpoints). `main.py` only creates the app and plugs in the routes.
- **Keycloak** is the identity provider. It runs as a Compose service and imports a `capstone` realm with roles `admin` and `user` and two test users. The backend downloads Keycloak's public keys and verifies each token itself. It reads the role from `realm_access.roles`, with no second database lookup.
- **Keycloak stores its data in PostgreSQL.** It has its own database container (`keycloak-db`) with a named volume, so its realm, users and roles survive a restart. The realm file is imported only on the first start, so later changes are never overwritten.
- **PostgreSQL (`db`)** stores which Keycloak user owns which candidate id, and the candidate records.
- **MinIO** stores the uploaded images and the generated PDFs.
- **Docker Compose** runs all five services from one file. Configuration lives in `.env` and is referenced once with `${VAR}`. Services find each other by name. Neither database publishes a port. Postgres, Keycloak's database and MinIO each have a named volume.

## What I tested
- Fresh start with `docker compose up -d --build`; all services Up.
- No token gives 401; a normal user calling an admin endpoint gives 403; an admin gets 200 or 201.
- A candidate can only open the report for the candidate id linked to their own Keycloak user (another user gets 403).
- Full CRUD on `/candidates`, with validation errors (422), duplicates (409) and missing ids (404).
- `docker compose down` then `up -d`: candidates, uploaded documents and Keycloak users were all still there.

## What is rough
- Token issuer and audience checks are switched off in `core/security.py` because the issuer differs inside Docker (`keycloak:8080` versus `localhost:8080`). Signature and expiry are still checked.
- OCR plus pattern matching is a heuristic. An unusual certificate layout gives "UNABLE TO VERIFY". A match does not prove a document is genuine.
- Dependency versions are not pinned.
- Temporary files are not deleted after a report is created.
- The OCR loop ignores a failed pass silently instead of logging it.
- There is no frontend yet and no automated tests.
- A new database connection is opened for each call (no pool).
- Demo passwords are written in plain text in the realm file and helper scripts; they are for local test users only.

## What I would do next
Pin versions, validate the token issuer, clean up temporary files, log OCR errors, add pytest tests, accept PDF uploads, and build a simple frontend with a navigation bar, tabs and forms.
