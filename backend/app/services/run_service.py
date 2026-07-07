from fastapi import HTTPException
from backend.app.repositories import run_repository

def list_runs(session, limit=20, offset=0, result=None, min_coverage=None):
    return run_repository.get_all_runs(session, limit, offset, result, min_coverage)

def get_run(session, run_id: int):
    run = run_repository.get_run_by_id(session, run_id)
    if(run is None):
        raise HTTPException(status_code=404, detail="Run not found")
    
    for cp in run.coverpoints:
        cp.total_bins = len(cp.bins)
        cp.missed_bins = sum(1 for b in cp.bins if not b.hit)

    run.total_bins = sum(cp.total_bins for cp in run.coverpoints)
    run.missed_bins = sum(cp.missed_bins for cp in run.coverpoints)
    return run
