CREATE TABLE IF NOT EXISTS candidate_user_mapping (
    candidate_id     TEXT PRIMARY KEY,
    keycloak_user_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS candidates (
    candidate_id TEXT PRIMARY KEY,
    full_name    TEXT NOT NULL,
    email        TEXT NOT NULL,
    status       TEXT NOT NULL DEFAULT 'PENDING',
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);
