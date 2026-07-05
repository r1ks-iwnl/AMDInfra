from sqlalchemy import (Integer, String, DateTime,
                        Numeric, Boolean, ForeignKey, 
                        func, create_engine, event)
from sqlalchemy.orm import (DeclarativeBase, mapped_column, relationship, sessionmaker)
from sqlalchemy.engine import Engine


DATABASE_URL = "sqlite:///database/app.db"

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autoflush=False, bind=engine)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class Base(DeclarativeBase):
    pass

class Run(Base):
    __tablename__ = "runs"
    id = mapped_column(Integer, primary_key=True)
    filename = mapped_column(String, nullable=False)
    run_date = mapped_column(DateTime, nullable=False, index=True)
    result = mapped_column(String, nullable=False)
    checks = mapped_column(Integer)
    overall_coverage = mapped_column(Numeric(5,2))
    uploaded_at = mapped_column(DateTime, server_default=func.now())
    uploaded_by = mapped_column(String)
    coverpoints = relationship("Coverpoint", back_populates="run",
                               cascade="all, delete-orphan", passive_deletes=True)
    
class Coverpoint(Base):
    __tablename__ = "coverpoints"
    id = mapped_column(Integer, primary_key=True)
    run_id = mapped_column(ForeignKey("runs.id", ondelete="CASCADE"))
    name = mapped_column(String, nullable=False)
    coverage = mapped_column(Numeric(5,2))
    run = relationship("Run", back_populates="coverpoints")
    bins = relationship("Bin", back_populates="coverpoint",
                        cascade="all, delete-orphan")
    
class Bin(Base):
    __tablename__ = "bins"
    id = mapped_column(Integer, primary_key=True)
    coverpoint_id = mapped_column(ForeignKey("coverpoints.id", ondelete="CASCADE"))
    name = mapped_column(String, nullable=False)
    value = mapped_column(String, nullable=True)
    hits = mapped_column(Integer, nullable=False)
    hit = mapped_column(Boolean, nullable=False)
    coverpoint = relationship("Coverpoint", back_populates="bins")
