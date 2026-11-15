
import psycopg

from app.core.config import DATABASE_URL


def db_connect():
    """Open a new PostgreSQL connection using the capstone schema."""
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not configured")

    conn = psycopg.connect(DATABASE_URL)

    # Use capstone schema instead of public
    conn.execute("SET search_path TO capstone")

    return conn
