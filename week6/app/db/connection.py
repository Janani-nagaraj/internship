import psycopg

from app.core.config import DATABASE_URL


def db_connect():
    """Open a new PostgreSQL connection from the DATABASE_URL setting."""
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not configured")
    return psycopg.connect(DATABASE_URL)
