from backend.app.repositories import run_repository

from ..parser.coverage_parser import parse_text
from database import Run, Coverpoint, Bin

def list_runs(session, limit=20, offset=0, result=None, min_coverage=None):
    return run_repository.get_all_runs(session, limit, offset, result, min_coverage)

def get_run(session, run_id: int):
    return run_repository.get_run_by_id(session, run_id)

def create_run_from_log(session, filename, text, uploaded_by = None):
    report = parse_text(text)
    
    run = Run(filename = filename, run_date = report.run_datetime, result = report.result,
              checks = report.checks, overall_coverage = float(report.overall_coverage), uploaded_by = uploaded_by)
    
    for cp in report.coverpoints:
        coverpoint = Coverpoint(name = cp.name, coverage = float(cp.coverage))

        for b in cp.bins:
            coverpoint.bins.append(Bin(name = b.name, value = b.value, hits = b.hits, hit = b.hit))

        run.coverpoints.append(coverpoint)

    run_repository.create_run(session, run) 

    return run
