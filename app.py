#20250814PM2041,雅
# app.pPMy
from sqlalchemy import text
import os, json
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, Body, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db import Base, engine, SessionLocal
from models import Oath, Heartbeat, Event
from deps import get_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/db/health")
def db_health():
    try:
        with SessionLocal() as s:
            # SQLAlchemy 2.0 規則：字串 SQL 要用 text(...)
            s.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        # 先回報錯誤訊息，方便在 Logs 看到真正原因
        raise HTTPException(status_code=500, detail=f"db connection failed: {e}")


# --- Oath 基礎 ---
@app.post("/oath")
def upsert_oath(content: str = Body(..., embed=True), db: Session = Depends(get_db)):
    oath = db.query(Oath).filter_by(name="baseline").first()
    if oath:
        oath.content = content
    else:
        oath = Oath(name="baseline", content=content)
        db.add(oath)
    db.commit()
    db.refresh(oath)
    return {"status": "ok", "oath_id": oath.id}

@app.get("/oath")
def get_oath(db: Session = Depends(get_db)):
    oath = db.query(Oath).filter_by(name="baseline").first()
    if not oath:
        return JSONResponse({"status": "empty", "content": ""})
    return {"status": "ok", "content": oath.content, "updated_at": oath.updated_at}

# --- Heartbeat ---
@app.post("/heartbeat")
def post_heartbeat(
    note: str = Body("", embed=True),
    payload: dict | None = Body(None),
    db: Session = Depends(get_db),
):
    hb = Heartbeat(note=note, payload=payload or {})
    db.add(hb)
    db.commit()
    db.refresh(hb)
    return {"status": "ok", "id": hb.id}

@app.get("/heartbeat/latest")
def latest_heartbeat(db: Session = Depends(get_db)):
    hb = db.query(Heartbeat).order_by(Heartbeat.id.desc()).first()
    if not hb:
        return JSONResponse({"status": "empty"})
    return {
        "status": "ok",
        "id": hb.id,
        "note": hb.note,
        "utc_time": hb.utc_time,
        "payload": hb.payload or {},
    }

# --- Event（可選）---
@app.post("/event")
def post_event(
    tag: str = Body(..., embed=True),
    title: str = Body(..., embed=True),
    detail: str = Body("", embed=True),
    db: Session = Depends(get_db),
):
    ev = Event(tag=tag, title=title, detail=detail)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return {"status": "ok", "id": ev.id}
