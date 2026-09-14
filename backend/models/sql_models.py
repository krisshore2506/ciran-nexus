from sqlalchemy import Column, String, Integer, DateTime, JSON, ARRAY, ForeignKey
from pgvector.sqlalchemy import Vector
from config.db import Base
from datetime import datetime

class RawRecord(Base):
    __tablename__ = "raw_records"

    id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False, index=True)
    timestamp = Column(String, nullable=False)
    source_system = Column(String, nullable=False)
    content = Column(JSON, nullable=False)

class Entity(Base):
    __tablename__ = "entities"

    id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False, index=True)
    label = Column(String, nullable=False)
    subtitle = Column(String, nullable=False)
    priority = Column(Integer, nullable=True)
    priorityBand = Column(String, nullable=True)
    cases = Column(ARRAY(String), nullable=True)
    relationships = Column(Integer, nullable=True)
    recentEvents = Column(Integer, nullable=True)
    attributes = Column(JSON, nullable=True) # List[Attribute]
    priorityFactors = Column(JSON, nullable=True) # List[PriorityFactor]

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, index=True)
    severity = Column(String, nullable=False)
    title = Column(String, nullable=False)
    explanation = Column(String, nullable=False)
    case_id = Column(String, nullable=False) # Maps to domain 'case'
    timestamp = Column(String, nullable=False)
    confidence = Column(Integer, nullable=False)
    entities = Column(ARRAY(String), nullable=False)

class EvidenceItem(Base):
    __tablename__ = "evidence_items"

    id = Column(String, primary_key=True, index=True)
    insight = Column(String, nullable=False)
    sources = Column(JSON, nullable=False) # List[EvidenceSource]
    analysis = Column(String, nullable=False)
    relationship = Column(String, nullable=False)
    status = Column(String, nullable=False)
    audit = Column(JSON, nullable=False) # List[EvidenceAudit]

class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(String, primary_key=True, index=True)
    date = Column(String, nullable=False)
    day = Column(String, nullable=False)
    category = Column(String, nullable=False)
    title = Column(String, nullable=False)
    detail = Column(String, nullable=False)
    entities = Column(ARRAY(String), nullable=False)
    record = Column(String, nullable=False)
    crimeType = Column(String, nullable=True)

class PatternInsight(Base):
    __tablename__ = "pattern_insights"

    id = Column(String, primary_key=True, index=True)
    category = Column(String, nullable=False)
    title = Column(String, nullable=False)
    entities = Column(ARRAY(String), nullable=False)
    path = Column(ARRAY(String), nullable=True)
    confidence = Column(Integer, nullable=False)
    why = Column(String, nullable=False)
    evidence = Column(ARRAY(String), nullable=False)

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(String, primary_key=True, index=True)
    record_id = Column(String, ForeignKey("raw_records.id"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    text_content = Column(String, nullable=False)
    embedding = Column(Vector(1536), nullable=True)
    timestamp = Column(String, nullable=False)
