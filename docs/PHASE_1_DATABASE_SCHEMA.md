# Phase 1: Database Schema

## PostgreSQL Schema (SQLAlchemy)

### 1. `raw_records`
Stores original JSON documents ensuring traceability.
- `id` (String, PK)
- `type` (String)
- `timestamp` (String)
- `source_system` (String)
- `content` (JSON)

### 2. `entities`
Source of truth for all entities (Persons, Vehicles, Cases, Phones, etc.).
- `id` (String, PK) - **Identical to Neo4j Node ID**
- `type` (String) - e.g., 'person', 'case'
- `label` (String)
- `subtitle` (String)
- `priority` (Integer, Nullable)
- `priorityBand` (String, Nullable)
- `cases` (Array of Strings) - Case IDs this entity is involved in.
- `attributes` (JSON) - Detailed entity attributes.
- `priorityFactors` (JSON) - Explanation of risk scores.

### 3. Additional Analysis Tables
- `alerts`: System-generated intelligence alerts.
- `evidence_items`: Documented findings.
- `timeline_events`: Temporal events for rendering the timeline UI.
- `pattern_insights`: Detected anomalies and patterns.

---

## Neo4j Graph Schema

### Nodes
Nodes directly mirror `Entity` objects in PostgreSQL.
- **Labels**: `:Person`, `:Phone`, `:Vehicle`, `:Account`, `:Location`, `:Case`
- **Properties**: 
  - `id`: Unique identifier identical to PostgreSQL `Entity.id`.
  - `label`: Display name.

### Relationships
Relationships are established between nodes.
- **Types**: `:COMMUNICATION`, `:FINANCIAL`, `:VEHICLE`, `:LOCATION`, `:CASE_ASSOCIATION`
- **Properties**:
  - `sourceRecord`: RawRecord ID that serves as evidence.
  - `confidence`: Integer (0-100).
  - `timestamp`: String (if applicable).
