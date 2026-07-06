import sys
from pathlib import Path

_DB_DIR = str(Path(__file__).parent.resolve())
if _DB_DIR not in sys.path:
    sys.path.insert(0, _DB_DIR)

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

from base import Base
from models import Run, Coverpoint, Bin

DATABASE_URL = "sqlite:///database/app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autoflush=False, bind=engine)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
