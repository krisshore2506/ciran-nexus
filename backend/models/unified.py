from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

# Constants for common types to ensure standardization
UnifiedEntityType = Literal[
    "PERSON", 
    "ACCOUNT", 
    "PHONE", 
    "CASE", 
    "LOCATION", 
    "VEHICLE", 
    "ORGANIZATION", 
    "CELL_TOWER"
]

UnifiedRelationshipType = Literal[
    "COMMUNICATION", 
    "TRANSACTION", 
    "INVOLVED_IN", 
    "LOCATED_AT", 
    "ASSOCIATED_WITH", 
    "OCCURRED_AT"
]

MatchStatus = Literal["MATCHED", "POSSIBLE_MATCH", "NOT_MATCHED"]

class Provenance(BaseModel):
    source_dataset: str
    source_file: str
    source_record_id: str

class Location(BaseModel):
    location_id: str
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    cell_id: Optional[str] = None

class UnifiedEntity(BaseModel):
    entity_id: str
    entity_type: UnifiedEntityType
    label: str
    identifiers: Dict[str, str] = Field(default_factory=dict)
    attributes: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    match_status: MatchStatus = "NOT_MATCHED"

class UnifiedRelationship(BaseModel):
    relationship_id: str
    source_entity: str
    target_entity: str
    relationship_type: UnifiedRelationshipType
    timestamp: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    source_record_ids: List[str] = Field(default_factory=list)

class SourceRecord(BaseModel):
    source_record_id: str
    source_dataset: str
    record_type: str
    timestamp: Optional[str] = None
    entities: List[UnifiedEntity] = Field(default_factory=list)
    relationships: List[UnifiedRelationship] = Field(default_factory=list)
    location: Optional[Location] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    provenance: Provenance
