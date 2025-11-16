from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from routes.resume_route import router as resume_router
from routes.jd_routes import router as jd_router
from routes.user_routes import router as user_router

from models.base import Base, engine, session
import models
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")
    yield
    engine.dispose()
    session.close()
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)


@app.get("/health_check")
async def health_check():
    return {"status": "ok"}


app.include_router(resume_router, tags=["Resume"])

app.include_router(jd_router, tags=["Job Description"])
app.include_router(user_router, tags=["User"])

