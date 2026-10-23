import psycopg
from fastapi import HTTPException

from config import DATABASE_URL


def db_connect():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not configured")
    return psycopg.connect(DATABASE_URL)


def register_candidate_owner(candidate_id: str, keycloak_user_id: str):
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO candidate_user_mapping (candidate_id, keycloak_user_id)
                VALUES (%s, %s)
                ON CONFLICT (candidate_id)
                DO UPDATE SET keycloak_user_id = EXCLUDED.keycloak_user_id
                WHERE candidate_user_mapping.keycloak_user_id = EXCLUDED.keycloak_user_id
                """,
                (candidate_id, keycloak_user_id),
            )
            if cur.rowcount != 1:
                raise ValueError("Candidate ID is already linked to another Keycloak user.")


def ensure_candidate_owner(candidate_id: str, keycloak_user_id: str):
    with db_connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT keycloak_user_id FROM candidate_user_mapping WHERE candidate_id = %s",
                (candidate_id,),
            )
            row = cur.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Candidate ID '{candidate_id}' was never registered. Run /report-0 first.",
        )
    if row[0] != keycloak_user_id:
        raise HTTPException(
            status_code=403,
            detail=(
                "This candidate ID belongs to a different Keycloak user. "
                "Use the token of the user whose ID was entered in /report-0."
            ),
        )
