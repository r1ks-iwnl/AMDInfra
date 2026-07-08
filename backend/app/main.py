from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import runs

from .config import get_settings

settings = get_settings()

app = FastAPI(title="Functional Coverage Dashboard",
            description="API for managing and analysis of hardware functional coverage reports.",
            version="1.0.0")

app.add_middleware(CORSMiddleware,
                   allow_origins=[settings.FRONTEND_ORIGIN],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(runs.router, prefix="/runs")

@app.get("/")
def health_check():
    return {"status": "ok"}
