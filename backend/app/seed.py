import glob, os

from sqlalchemy.orm import Session
from database.database import Run, Coverpoint, Bin, SessionLocal
from backend.app.parser.coverage_parser import parse_file

def seed(session: Session, log_path: str):
    run_exists = session.query(Run).filter_by(filename=log_path).first()
    if(run_exists):
        print(f"Skipped {log_path}: Already exists.")
        return

    print(f"Parsing {log_path}...")

    report = parse_file(log_path)

    run = Run(filename = log_path,
              run_date = report.run_datetime,
              result = report.result, checks = report.checks,
              overall_coverage = report.overall_coverage)
    for cp in report.coverpoints:
        c = Coverpoint(name=cp.name, coverage=cp.coverage)
        c.bins = [Bin(name = b.name, value = b.value,
                      hits = b.hits, hit = b.hit) for b in cp.bins]
        run.coverpoints.append(c)

    session.add(run)

def main():
    log_folder = "logs"
    log_files = glob.glob(os.path.join(log_folder, "*.txt"))

    if(not log_files):
        print(f"[Warning] No log files found.")
    else:
        print(f"Processing {len(log_files)} log files.")

    with SessionLocal() as session:
        for log in log_files:
            seed(session, log)

        session.commit()
        print("[Success] Database seeded.")

if(__name__ == "__main__"):
    main()