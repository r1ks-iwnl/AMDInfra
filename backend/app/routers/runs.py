from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from backend.app.services import run_service
from ..schemas.run import RunDetail, RunSummary

router = APIRouter()

# list endpoint returns more than one run -> the response model must be a list
@router.get("/", response_model=list[RunSummary])
def list_runs(limit: int = 20, offset: int = 0, result=None, min_coverage=None, db=Depends(get_db)):
    return run_service.list_runs(db, limit, offset, result, min_coverage)

@router.get("/{run_id}", response_model=RunDetail)
def get_run(run_id: int, db=Depends(get_db)):
    run = run_service.get_run(db, run_id)
    if run is None:
        # HTTP concerns live in the router, not the service
        raise HTTPException(status_code=404, detail="Run not found")
    return run
