#20250810pM2050,雅
# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, UniqueConstraint
from sqlalchemy.sql import func
from db import Base

class Oath(Base):
    __tablename__ = "oaths"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), default="baseline", unique=True)
    content = Column(Text, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Heartbeat(Base):
    __tablename__ = "heartbeats"
    id = Column(Integer, primary_key=True)
    note = Column(String(255), default="")
    utc_time = Column(DateTime(timezone=True), server_default=func.now())
    payload = Column(JSON)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    tag = Column(String(64), index=True)
    title = Column(String(255))
    detail = Column(Text)
    utc_time = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint('tag', 'utc_time', name='uq_tag_time'),)
