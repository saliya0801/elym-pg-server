# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from db import Base

class Oath(Base):
    __tablename__ = "oaths"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, default="baseline")
    content = Column(Text, nullable=False, default="")
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Heartbeat(Base):
    __tablename__ = "heartbeats"
    id = Column(Integer, primary_key=True, index=True)
    note = Column(String(255), default="")
    utc_time = Column(DateTime(timezone=True), server_default=func.now())
    payload = Column(JSON)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String(64), index=True)
    title = Column(String(255))
    detail = Column(Text)
    utc_time = Column(DateTime(timezone=True), server_default=func.now())
