#20250810PM2052,雅
# deps.py
from db import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
