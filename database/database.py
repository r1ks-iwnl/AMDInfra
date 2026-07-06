from sqlalchemy import (Integer, String, DateTime,
                        Numeric, Boolean, ForeignKey, 
                        func, create_engine, event)
from sqlalchemy.orm import (DeclarativeBase, mapped_column, Mapped, relationship, sessionmaker)
from sqlalchemy.engine import Engine
from datetime import datetime
from decimal import Decimal


DATABASE_URL = "sqlite:///database/app.db"

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
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

class Base(DeclarativeBase):
    pass

class Run(Base):
    __tablename__ = "runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    run_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    result: Mapped[str] = mapped_column(String, nullable=False)
    checks: Mapped[int] = mapped_column(Integer)
    overall_coverage: Mapped[Decimal] = mapped_column(Numeric(5,2))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    uploaded_by: Mapped[str | None] = mapped_column(String, nullable=True)
    coverpoints: Mapped[list["Coverpoint"]] = relationship("Coverpoint", back_populates="run",
                               cascade="all, delete-orphan", passive_deletes=True)
    
class Coverpoint(Base):
    __tablename__ = "coverpoints"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    coverage: Mapped[Decimal] = mapped_column(Numeric(5,2))
    run: Mapped["Run"] = relationship("Run", back_populates="coverpoints")
    bins: Mapped[list["Bin"]] = relationship("Bin", back_populates="coverpoint",
                        cascade="all, delete-orphan", passive_deletes=True)
    
class Bin(Base):
    __tablename__ = "bins"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    coverpoint_id: Mapped[int] = mapped_column(ForeignKey("coverpoints.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str | None] = mapped_column(String, nullable=True)
    hits: Mapped[int] = mapped_column(Integer, nullable=False)
    hit: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coverpoint: Mapped["Coverpoint"] = relationship("Coverpoint", back_populates="bins")
