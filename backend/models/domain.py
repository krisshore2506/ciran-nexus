from typing import List, Optional, Literal
from pydantic import BaseModel, Field

EntityType = Literal["person", "phone", "vehicle", "account", "location", "case", "organization", "date", "cell_tower"]
RelationType = Literal["communication", "financial", "vehicle", "location", "case", "organization", "SAME_AS", "POSSIBLE_MATCH"]
Severity = Literal["critical", "high", "medium", "info"]

class Attribute(BaseModel):
    label: str
    value: str

class PriorityFactor(BaseModel):
    label: str
    weight: int

class Entity(BaseModel):
    id: str
    type: EntityType
    label: str
    subtitle: str
    priority: Optional[int] = None
    priorityBand: Optional[Literal["HIGH", "MEDIUM", "LOW"]] = None
    cases: Optional[List[str]] = None
    relationships: Optional[int] = None
    recentEvents: Optional[int] = None
    attributes: Optional[List[Attribute]] = None
    priorityFactors: Optional[List[PriorityFactor]] = None

class Relation(BaseModel):
    source: str
    target: str
    type: RelationType
    label: str
    confidence: int
    sourceRecord: str
    timestamp: Optional[str] = None

class TimelineEvent(BaseModel):
    id: str
    date: str
    day: str
    category: RelationType
    title: str
    detail: str
    entities: List[str]
    record: str

class Alert(BaseModel):
    id: str
    severity: Severity
    title: str
    explanation: str
    case: str
    timestamp: str
    confidence: int
    entities: List[str]

class EvidenceSource(BaseModel):
    id: str
    type: str
    timestamp: str

class EvidenceAudit(BaseModel):
    stage: str
    actor: str
    timestamp: str
    note: Optional[str] = None

class EvidenceItem(BaseModel):
    id: str
    insight: str
    sources: List[EvidenceSource]
    analysis: str
    relationship: str
    status: Literal["Pending Analyst Review", "Accepted", "Rejected"]
    audit: List[EvidenceAudit]

class SharedAttribute(BaseModel):
    type: str
    value: str

class CrossCaseLink(BaseModel):
    cases: List[str]
    shared: List[SharedAttribute]
    path: List[str]
    confidence: int
    evidence: List[str]
    summary: str

class PatternInsight(BaseModel):
    id: str
    category: str
    title: str
    entities: List[str]
    path: Optional[List[str]] = None
    confidence: int
    why: str
    evidence: List[str]

class CopilotTimelineItem(BaseModel):
    day: str
    title: str

class CopilotResponse(BaseModel):
    summary: str
    chips: List[str]
    path: Optional[List[str]] = None
    timeline: Optional[List[CopilotTimelineItem]] = None
    evidence: Optional[List[str]] = None
    confidence: int
    caution: Optional[str] = None

class RawRecord(BaseModel):
    id: str
    type: str
    timestamp: str
    content: dict
    source_system: str
