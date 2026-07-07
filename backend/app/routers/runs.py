from fastapi import APIRouter, Depends
from database import get_db
from backend.app.services import run_service
from ..schemas.run import RunDetail, RunSummary

router = APIRouter()

@router.get("/", response_model=RunSummary)
def list_runs(limit: int = 20, offset: int = 0, result=None, min_coverage=None, db=Depends(get_db)):
    return run_service.list_runs(db, limit, offset, result, min_coverage)

@router.get("/{run_id}", response_model=RunDetail)
def get_run(run_id: int, db=Depends(get_db)):
    return run_service.get_run(db, run_id)
