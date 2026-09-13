# PHASE 0: PHASE 1 HANDOFF

This document outlines the critical elements that must be prepared and understood before commencing Phase 1 (PostgreSQL + Neo4j Integration).

## 1. Existing Pydantic Models
The models in `backend/models/domain.py` (`Entity`, `Relation`, `Alert`, `EvidenceItem`, `TimelineEvent`, `PatternInsight`, `CrossCaseLink`) are well-defined and must be mapped 1-to-1 to SQLAlchemy ORM models (for PostgreSQL) and Node/Edge schemas (for Neo4j).

## 2. IDs & Primary Keys
Currently, string IDs (e.g., `"P1"`, `"C1"`) are used universally in the mock data. When transitioning to a database, consider retaining string-based UUIDs or structured IDs to ensure compatibility with Neo4j graph nodes.

## 3. Relationships & Data Types
The `Relation` model has `source` and `target` linking to Entity IDs, with a specific `type` enum (`communication`, `financial`, `vehicle`, etc.). These MUST become explicit edges in Neo4j (e.g., `(a:Person)-[:COMMUNICATION]->(b:Person)`).

## 4. Missing Fields
- **Authentication**: No user/officer model exists yet. Need to add a `User` model with RBAC fields for login functionality.
- **Raw Document Storage**: Need a table to store unstructured raw text inputs before entity extraction occurs.

## 5. State Dependencies
The `state.py` singleton currently handles all CRUD operations implicitly. Phase 1 must introduce a Repository pattern or direct DB session injection (via FastAPI `Depends`) to replace `state.entities` with `db.query(Entity).all()` and Neo4j driver queries.

## 6. Frontend API Assumptions
The frontend expects rapid, synchronous JSON responses matching the current Pydantic models. Database queries must be optimized (e.g., eager loading) to maintain the current response shape, ensuring the UI does not break during the backend migration.
