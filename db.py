#20250814PM1717,雅
# db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "")

# 在啟動 log 印出是否抓到（避免洩密，只印主機段）
if not DATABASE_URL:
    print("[BOOT] DATABASE_URL is MISSING", flush=True)
else:
    try:
        hostpart = DATABASE_URL.split("@", 1)[1].split("/", 1)[0]
    except Exception:
        hostpart = "(parse-failed)"
    print(f"[BOOT] DATABASE_URL detected → {hostpart}", flush=True)

# 沒變數就先不要建立 engine，讓應用仍可啟動
engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True) if DATABASE_URL else None
SessionLocal = (sessionmaker(bind=engine, autoflush=False, autocommit=False) if engine else None)
Base = declarative_base()
