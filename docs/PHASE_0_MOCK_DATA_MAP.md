# PHASE 0: MOCK DATA MAP

## synthetic_data.json
↓
**WHAT DATA IT PROVIDES:**
Mock RawRecords containing nested dictionaries representing persons, locations, cases, and vehicles.
↓
**WHO USES IT:**
Backend `ingestion.py` route `/api/ingestion/load`.
↓
**CURRENT PURPOSE:**
Populates the in-memory `state.py` with the initial graph of entities and relationships.
↓
**PHASE WHERE IT WILL BE REPLACED:**
Phase 1 (Replaced by a seed script inserting records directly into PostgreSQL and Neo4j).

---

## ciran-data.ts (Frontend)
↓
**WHAT DATA IT PROVIDES:**
Hardcoded node layout coordinates (`nodePositions`), mock datasets (`mockInvestigations`, `mockEvidence`, etc.), and typography/type mappings.
↓
**WHO USES IT:**
Frontend `NetworkGraph`, `timeline.tsx`, `investigations.tsx`, and `ciran-service.ts`.
↓
**CURRENT PURPOSE:**
Provides static visualization constraints and fallbacks for UI development without a real API.
↓
**PHASE WHERE IT WILL BE REPLACED:**
Phase 2/3 (Dynamic graph replacement will remove the need for hardcoded coordinates).

---

## Backend Ingestion Logic (`ingestion.py`)
↓
**WHAT DATA IT PROVIDES:**
Simulated entity extraction and graph building logic.
↓
**WHO USES IT:**
The FastAPI server startup hook (`lifespan`) and manual `/load` endpoint.
↓
**CURRENT PURPOSE:**
Fakes an ETL pipeline by iterating over `synthetic_data.json`.
↓
**PHASE WHERE IT WILL BE REPLACED:**
Phase 2 (Replaced by actual File Upload + NLP Entity Extraction using OpenAI/SpaCy).
