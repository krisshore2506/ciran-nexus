# PHASE 0: STATE DEPENDENCY MAP

## The Core State Module
`state.py` (Singleton instance: `state`)

## Downstream Dependencies

### 1. Ingestion Pipeline
`state.py`
 ↓
`ingestion.py`
 ↓
Populates `entities`, `relations`, `timeline`, `patterns`, `cross_case_links`, `evidence`, and `alerts`.

### 2. API Routes
`state.py`
 ↓
`api/routes/entities.py`, `network.py`, `cases.py`, `alerts.py`, `patterns.py`, `cross_case.py`, `evidence.py`, `copilot.py`, `reports.py`, `kpis.py`, `timeline.py`
 ↓
Provides JSON responses to Frontend API calls.

### 3. AI Copilot Service
`state.py`
 ↓
`routes/copilot.py`
 ↓
`llm_service.py`
 ↓
`copilot_retrieval.py`
 ↓
Filters the in-memory arrays (`state.entities`, `state.relations`) to build the RAG context window for the OpenAI prompt.

### 4. Graph & Risk Services
`state.py` (via `relationship_engine`)
 ↓
`graph_intelligence.py`, `correlation_engine.py`, `risk_engine.py`
 ↓
Executes synchronous BFS traversal and heuristic ranking over Python dictionaries stored in the singleton.
