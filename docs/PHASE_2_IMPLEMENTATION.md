# Phase 2 Implementation: Real Data Processing

## Overview
Phase 2 establishes the pipeline for ingesting unstructured text and structural files directly into PostgreSQL (as the source of truth) and Neo4j (as the network relationship graph). The objective is to replace the mock memory data system while establishing a secure, traceable, and deterministic pipeline for future agents.

## Supported File Formats
- `TXT` (Plain Text, UTF-8)
- `PDF` (Parsed via PyPDF2)
- `JSON` (Flattened for text analysis)
- `CSV` (Flattened for text analysis)

## Ingestion Architecture

The `IngestionService` orchestrates the pipeline:

1. **Document Parse:** Extracts text securely without executing files.
2. **Raw Record Creation:** Creates a `RawRecord` in PostgreSQL in `PROCESSING` state to ensure every document is tracked even if extraction fails.
3. **NLP Extraction:** Extracts entities and relationships.
4. **Entity Resolution:** Strictly deduplicates entities against PostgreSQL.
5. **Persistence:** Saves mapped nodes and edges into PostgreSQL and Neo4j.
6. **Status Update:** Marks `RawRecord` as `SUCCESS`.

## Entity Extraction Approach
The extraction is handled by `NLPExtractor`:
- **Primary:** Utilizes the configured OpenAI LLM (`gpt-4o-mini`) requesting a strict structured JSON output to extract entities (Person, Vehicle, Phone, Location, Account, Case) and their explicit relationships.
- **Fallback:** Uses deterministic Python regex rules to securely extract structured patterns (e.g. phones, specific cases, known mock persons). The fallback NEVER invents relationships. 

## Entity Resolution Approach
The resolution is handled by `IdentityResolver`:
- Implements strict identity matching.
- Only exact, normalized identifiers (type and label) will match an existing PostgreSQL `Entity`.
- Avoids false merges (e.g., merging "R. Kumar" with "Ravi Kumar" automatically without strong evidence).
- Preserves globally deterministic IDs.

## Persistence
- **PostgreSQL:** `RawRecord` (for audit and original text) and `Entity` (for deduplicated profiles).
- **Neo4j:** Nodes (matching Postgres IDs) and Edges (Relationships with `sourceRecord` linking back to the `RawRecord` for complete traceability).

## API Endpoints
- `POST /api/upload`: Accepts `multipart/form-data`. Returns JSON summary of processing.

### Example Request
```bash
curl -X POST -F "file=@case_notes.txt" http://localhost:8000/api/upload
```

### Example Response
```json
{
  "status": "success",
  "record_id": "DOC-A1B2C3D4",
  "entities_extracted": 3,
  "relationships_extracted": 2
}
```

## Known Limitations
- Background processing is not yet implemented (Processing is synchronous for small documents).
- PDF extraction relies on `PyPDF2`, which does not support image-based PDFs (OCR).

## Future Improvements
- Implement async task queue (e.g., Celery) for large files.
- Move towards advanced LangGraph agents for multi-step contextual processing.
