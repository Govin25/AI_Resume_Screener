import asyncpg
import os


async def create_connection():
    """Create and return a connection to the PostgreSQL database."""
    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    conn = await asyncpg.connect(
        user=user, password=password, database=database, host=host, port=port
    )
    return conn


async def get_all_resumes():
    conn = await create_connection()

    rows = await conn.fetch("SELECT * FROM resumes ORDER BY created_at DESC;")
    await conn.close()

    return [dict(row) for row in rows]
