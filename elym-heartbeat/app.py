#20250810PM2049,雅
# app.py
import os, json
from fastapi import FastAPI, Depends, Body
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

from db import Base, engine
from models import Oath, Heartbeat, Event
from deps import get_db
from sqlalchemy.orm import Session

app = FastAPI()

# 啟動時自動建表
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# --- Oath（baseline 誓言） ---
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
    return {"status":"ok", "oath_id": oath.id}

@app.get("/oath")
def get_oath(db: Session = Depends(get_db)):
    oath = db.query(Oath).filter_by(name="baseline").first()
    if not oath:
        return JSONResponse({"status":"empty", "content":""})
    return {"status":"ok", "content": oath.content, "updated_at": oath.updated_at}

# --- Heartbeat（心跳） ---
@app.post("/heartbeat")
def post_heartbeat(
    note: str = Body("", embed=True),
    payload: dict | None = Body(None),
    db: Session = Depends(get_db),
):
    hb = Heartbeat(
        note=note,
        utc_time=datetime.now(timezone.utc),
        payload=payload or {}
    )
    db.add(hb)
    db.commit()
    db.refresh(hb)
    return {"status":"ok", "id": hb.id}

@app.get("/heartbeat/latest")
def get_latest_heartbeat(db: Session = Depends(get_db)):
    hb = db.query(Heartbeat).order_by(Heartbeat.id.desc()).first()
    if not hb:
        return JSONResponse({"status":"empty"})
    return {
        "status":"ok",
        "id": hb.id,
        "note": hb.note,
        "utc_time": hb.utc_time,
        "payload": hb.payload or {}
    }

# --- Event（可選） ---
@app.post("/event")
def post_event(
    tag: str = Body(..., embed=True),
    title: str = Body("", embed=True),
    detail: str = Body("", embed=True),
    db: Session = Depends(get_db)
):
    ev = Event(tag=tag, title=title, detail=detail)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return {"status":"ok", "id": ev.id}
