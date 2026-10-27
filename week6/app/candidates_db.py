from database import db_connect

COLUMNS = "candidate_id, full_name, email, status, created_at"


def _row_to_dict(row):
    return {
        "candidate_id": row[0],
        "full_name": row[1],
        "email": row[2],
        "status": row[3],
        "created_at": row[4],
    }


def _ensure_table(cur):
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS candidates (
            candidate_id TEXT PRIMARY KEY,
            full_name    TEXT NOT NULL,
            email        TEXT NOT NULL,
            status       TEXT NOT NULL DEFAULT 'PENDING',
            created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )


def create_candidate(candidate_id, full_name, email, status):
    with db_connect() as conn:
        with conn.cursor() as cur:
            _ensure_table(cur)
            cur.execute(
                f"""
                INSERT INTO candidates (candidate_id, full_name, email, status)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (candidate_id) DO NOTHING
                RETURNING {COLUMNS}
                """,
                (candidate_id, full_name, email, status),
            )
            row = cur.fetchone()
    if row is None:
        raise ValueError("Candidate ID already exists.")
    return _row_to_dict(row)


def list_candidates():
    with db_connect() as conn:
        with conn.cursor() as cur:
            _ensure_table(cur)
            cur.execute(f"SELECT {COLUMNS} FROM candidates ORDER BY created_at DESC")
            return [_row_to_dict(r) for r in cur.fetchall()]


def get_candidate(candidate_id):
    with db_connect() as conn:
        with conn.cursor() as cur:
            _ensure_table(cur)
            cur.execute(f"SELECT {COLUMNS} FROM candidates WHERE candidate_id = %s", (candidate_id,))
            row = cur.fetchone()
    return _row_to_dict(row) if row else None


def update_candidate(candidate_id, full_name, email, status):
    with db_connect() as conn:
        with conn.cursor() as cur:
            _ensure_table(cur)
            cur.execute(
                f"""
                UPDATE candidates SET full_name = %s, email = %s, status = %s
                WHERE candidate_id = %s
                RETURNING {COLUMNS}
                """,
                (full_name, email, status, candidate_id),
            )
            row = cur.fetchone()
    return _row_to_dict(row) if row else None


def delete_candidate(candidate_id):
    with db_connect() as conn:
        with conn.cursor() as cur:
            _ensure_table(cur)
            cur.execute("DELETE FROM candidates WHERE candidate_id = %s", (candidate_id,))
            deleted = cur.rowcount == 1
            cur.execute("DELETE FROM candidate_user_mapping WHERE candidate_id = %s", (candidate_id,))
    return deleted
