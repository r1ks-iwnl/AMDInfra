from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import runs, auth
from starlette.middleware.sessions import SessionMiddleware
from .config import get_settings

settings = get_settings()

app = FastAPI(
    title="Functional Coverage Dashboard",
    description="API for managing and analysis of hardware functional coverage reports.",
    version="1.0.0",
    swagger_ui_init_oauth={
        "clientId": settings.GOOGLE_CLIENT_ID,
        "appName": "Functional Coverage Dashboard",
        "usePkceWithAuthorizationCodeGrant": True,
        "scopes": "openid email profile"
    }
)

app.add_middleware(CORSMiddleware,
                   allow_origins=[settings.FRONTEND_ORIGIN],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)

app.include_router(runs.router, prefix="/runs")
app.include_router(auth.router, prefix="/auth")

@app.get("/")
def health_check():
    return {"status": "ok"}
