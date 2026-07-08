from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import runs

app = FastAPI(title="Functional Coverage Dashboard")

app.add_middleware(CORSMiddleware, 
                   # 5173 is the Vite dev server port; must match or the browser blocks the frontend (that's for when we have the frontend :) )
                   allow_origins=["http://localhost:5173"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(runs.router, prefix="/runs", tags=["runs"])

@app.get("/")
def health_check():
    return {"status": "ok"}
