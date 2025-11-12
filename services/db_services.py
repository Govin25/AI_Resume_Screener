import asyncpg
import os
from models.base import session
from models.resume import Resume
from sqlalchemy import desc


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


async def get_all_resume():

    resp = session.query(Resume).order_by(desc(Resume.created_at)).all()

    return resp
