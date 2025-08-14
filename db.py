#20250814PM1717,雅
# db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

raw_url = os.getenv("DATABASE_URL", "")

# 1) Railway 可能給 "postgres://..."，SQLAlchemy 2.x 要用 "postgresql+psycopg2://..."
if raw_url.startswith("postgres://"):
    fixed_url = raw_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif raw_url.startswith("postgresql://"):
    fixed_url = raw_url.replace("postgresql://", "postgresql+psycopg2://", 1)
else:
    fixed_url = raw_url  # 讓它照原樣（例如已是 postgresql+psycopg2://）

# 2) 安全偵錯：只印出開頭幾個字元與長度，不外洩密碼
if not fixed_url:
    print("[BOOT] DATABASE_URL is MISSING", flush=True)
else:
    head = fixed_url[:16]
    print(f"[BOOT] DATABASE_URL detected (head='{head}...', len={len(fixed_url)})", flush=True)

# 3) 沒有 URL 就不要建 Engine，避免拋例外
engine = create_engine(fixed_url, pool_pre_ping=True, future=True) if fixed_url else None
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) if engine else None
Base = declarative_base()
