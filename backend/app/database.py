import os
import sys
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# ------------------------------------------------------------
# 1️⃣  Force UTF-8 everywhere (safe for Japanese Windows)
# ------------------------------------------------------------
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PGCLIENTENCODING"] = "UTF8"
os.environ["LANG"] = "C.UTF-8"
os.environ["LC_ALL"] = "C.UTF-8"

# Fix stdout/stderr encoding only if needed (avoid double-wrapping)
if sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

# ------------------------------------------------------------
# 2️⃣  Load .env and get database URL
# ------------------------------------------------------------
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://admin:admin@172.18.225.17:5432/grocery_db",
)

# psycopg 3 uses "postgresql+psycopg://" as dialect
# so we ensure the correct prefix for SQLAlchemy
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

print("DATABASE_URL repr:", repr(DATABASE_URL))

# ------------------------------------------------------------
# 3️⃣  Create engine (psycopg3, fully UTF-8 safe)
# ------------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
    isolation_level="AUTOCOMMIT",
    connect_args={
        "options": "-c client_encoding=UTF8",
    },
)

# Force UTF-8 on every connection
@event.listens_for(engine, "connect")
def enforce_utf8(dbapi_conn, connection_record):
    try:
        with dbapi_conn.cursor() as cur:
            cur.execute("SET client_encoding TO 'UTF8'")
    except Exception:
        pass

# ------------------------------------------------------------
# 4️⃣  SQLAlchemy Session + Base
# ------------------------------------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency to get DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
