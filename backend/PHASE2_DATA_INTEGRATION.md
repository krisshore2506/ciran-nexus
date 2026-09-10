# CIRAN Phase 2: Data Integration Layer

## Overview

The Phase 2 Data Integration layer seamlessly connects four separate, highly realistic datasets into the Unified CIRAN Data Model without breaking the existing Phase 1 inference pipelines or API contracts.

**NOTE:** The datasets handled by this integration (Indian Crime Dataset, Email-Eu-core Temporal, ITU Synthetic CDR, PaySim) are strictly public, synthetic, or research datasets. They are _NOT_ real government criminal records.

## Unified Data Model

To harmonize disparate datasets, all ingestion passes through a set of unified definitions:

- **Common Entities**: `PERSON`, `ACCOUNT`, `PHONE`, `CASE`, `LOCATION`, `VEHICLE`, `ORGANIZATION`, `CELL_TOWER`.
- **Common Relationships**: `COMMUNICATION`, `TRANSACTION`, `INVOLVED_IN`, `LOCATED_AT`, `ASSOCIATED_WITH`, `OCCURRED_AT`.
- **SourceRecord**: Every normalized record encapsulates its derived `entities`, `relationships`, and a strict `provenance` block mapping back to the origin file and row.

## Entity Resolution Strategy

This phase implements a highly defensive entity resolution foundation to avoid polluting the intelligence graph with false positives:

1.  **Namespacing**: Entity IDs are heavily namespaced (e.g., `EMAIL-123` vs `PAYSIM-123`) to prevent accidental collisions.
2.  **No Automatic Merging**: Because the four datasets lack globally consistent keys (like a shared SSN or MSISDN across all tables), they remain in distinct graph populations. The AI engines will ONLY connect them if a genuine correlation arises in Phase 3.
3.  **Confidence & Match Status**: Explicit tracking of match confidence is now supported via fields like `match_status = "MATCHED" | "NOT_MATCHED"`.

## Dataset Specific Adapters

Adapters act as the translation layer between CSV/JSON and the `SourceRecord` unified model.

### 1. Indian Crime Dataset (`CrimeAdapter`)

- **Mapping**: Report Number -> `CASE` entity. City -> `LOCATION` entity.
- **Relationships**: `OCCURRED_AT` link between `CASE` and `LOCATION`.
- **Attributes**: Crime Code, Description, Victim Demographics, Weapon Used.

### 2. Email-Eu-core Temporal (`EmailAdapter`)

- **Mapping**: `source` and `destination` -> `ACCOUNT` entities.
- **Relationships**: `COMMUNICATION` between the two accounts, tagged with the exact temporal timestamp.

### 3. ITU Synthetic CDR (`CDRAdapter`)

- **Mapping**: `msisdn` -> `PHONE` entity. `cell_id` -> `CELL_TOWER` entity.
- **Relationships**: `LOCATED_AT` edge between the `PHONE` and `CELL_TOWER` at the exact event `datetime`.
- _Note: We do not fabricate subscriber-to-subscriber relationships as the raw dataset only maps phones to towers._

### 4. PaySim (`PaySimAdapter`)

- **Mapping**: `nameOrig` and `nameDest` -> `ACCOUNT` entities.
- **Relationships**: `TRANSACTION` edge recording the `amount`, `isFraud` flags, and type.
- **Memory Management**: Due to its massive size (~471 MB), this adapter uses Python's `csv.DictReader` to lazily **stream** records into memory chunk-by-chunk. It fully supports `max_rows` limitations.
- **Time Preservation**: The PaySim `step` (simulation hour) is strictly preserved as the timestamp—no artificial clock times are fabricated.

## Provenance

Traceability is strictly preserved throughout the backend pipeline:

1.  **Adapter**: Attaches `Provenance(dataset, file, original_row_id)` to the `SourceRecord`.
2.  **State Extraction**: The `RelationshipEngine` captures the `source_record_id` directly onto the `Relation` edge.
3.  **Cross-Case Correlation**: Edge source IDs flow into the AI insights.
4.  **Evidence Engine**: Re-constructs exactly which datasets and rows contributed to a given alert (Preserving the Phase 1 provenance fix).

## How to Run Ingestion

To load a specific dataset into the CIRAN graph, trigger the API endpoint:

```json
POST /api/ingestion/load
{
    "dataset": "paysim",
    "file_path": "path/to/paysim.csv",
    "max_rows": 10000
}
```

_If triggered without a body, the system defaults to the Phase 1 synthetic ingestion flow to maintain 100% frontend compatibility._
