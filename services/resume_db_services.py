import asyncpg


async def create_connection():
    conn = await asyncpg.connect(user='postgres', password='password',
                                 database='resume_screener', host='localhost', port=5434)
    return conn


async def get_all_resumes():
    conn = await create_connection()
    
    rows = await conn.fetch("SELECT * FROM resumes ORDER BY created_at DESC;")
    await conn.close()
    
    return [dict(row) for row in rows] 