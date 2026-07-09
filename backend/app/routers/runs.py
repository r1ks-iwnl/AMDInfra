from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from backend.app.services import run_service
from ..auth.dependencies import get_current_user
from ..schemas import RunDetail, RunSummary
from ..config import get_settings

settings = get_settings()

router = APIRouter()

# list endpoint returns more than one run -> the response model must be a list
@router.get("/", response_model=list[RunSummary], tags=["Runs"], summary="List runs.")
def list_runs(
    limit: int = 20, 
    offset: int = 0, 
    result: str | None = None, 
    min_coverage: float | None = Query(
        default=None, 
        ge=0.0,
        le=100.0
    ), 
    db=Depends(get_db),
    user_email: str = Depends(get_current_user)
):
    return run_service.list_runs(db, limit, offset, result, min_coverage)

@router.get("/{run_id}", response_model=RunDetail,
            responses={404: {"description": "Run doesn't exist"}},
            tags=["Runs"], summary="Obtain run details.")
def get_run(run_id: int, db=Depends(get_db), user_email: str = Depends(get_current_user)):
    run = run_service.get_run(db, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

@router.post("/upload", status_code=201, response_model=RunDetail, 
             responses={400: {"description": "File is empty"}, 413: {"description": "File is too large"}},
             tags=["Runs"], summary="Upload a .txt run log file.")
async def upload_run(file: UploadFile = File(), db: Session = Depends(get_db), 
                     user_email: str = Depends(get_current_user)):
    if(not file.filename or not file.filename.lower().endswith(".txt")):
        raise HTTPException(400, "Only .txt files are accepted")
    
    raw = await file.read()

    if(not raw):
        raise HTTPException(400, "File is empty")
    if(len(raw) > settings.max_upload_bytes):
        raise HTTPException(413, "File is too large")
    
    text = raw.decode("utf-8")

    try:
        return run_service.create_run_from_log(db, file.filename, text, user_email)
    except ValueError as exc:
        raise HTTPException(400, f"Log invalid: {exc}")
