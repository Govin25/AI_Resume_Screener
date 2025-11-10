from fastapi import FastAPI
from routes.resume_route import router as resume_router
from routes.jd_routes import router as jd_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


@app.get("/health_check")
async def health_check():
    return {"status": "ok"}


app.include_router(resume_router, tags=["Resume"])

app.include_router(jd_router, tags=["Job Description"])
