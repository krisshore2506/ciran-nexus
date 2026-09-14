# Phase 5 Implementation: LangGraph Orchestration

## Objective
Introduce LangGraph as the orchestration layer for CIRAN intelligence queries, bridging `VectorSearchService`, `Neo4jGraphService`, and `LLMService` deterministically without reintroducing legacy `state.py` dependencies.

## Architecture

1. **State**: `CIRANGraphState` is a pure `TypedDict` retaining solely orchestration context (`query_type`, `fused_context`, `evidence_status`, `errors`, `response`). It does NOT store database connections.
2. **Orchestrator**: `CIRANGraphService` compiles the `StateGraph` and exposes a unified `.invoke(query)` method. Database and Neo4j sessions are provided at runtime and isolated within the service boundary, not in state.
3. **Nodes**:
   - `query_understanding`: Classifies intent into `EVIDENCE`, `GRAPH`, or `MIXED` deterministically.
   - `vector_retrieval`: Wraps `VectorSearchService`.
   - `graph_retrieval`: Prepares graph context or awaits `context_fusion`.
   - `context_fusion`: Fuses vectors into provenance-checked graph records using `ContextBuilder`.
   - `evidence_validation`: Enforces `NO_EVIDENCE`, `PARTIAL_EVIDENCE`, or `SUFFICIENT_EVIDENCE`.
   - `generate_answer`: Reuses existing `LLMService` mapping to produce grounded Copilot responses.
   - `safe_no_evidence`: Fast-tracks unanswerable queries immediately to a constrained failure message.

## Routing Logic
- Uses `add_conditional_edges` to route `EVIDENCE` and `MIXED` to Vector paths.
- `MIXED` paths route through `graph_retrieval` sequentially.
- If Validation produces `NO_EVIDENCE`, the LLM is bypassed.

## Security & Safeguards
- Context strictly decoupled from `api.state.py` legacy mappings.
- No LLM generation allowed on `NO_EVIDENCE` status.
- Graph depth bounded by Phase 3 restrictions; Vector `top_k` bounded by Phase 4 restrictions.

## Tests & Runtime
- `backend/tests/test_langgraph.py` validates graph compilation, deterministic node outputs, and structural flow.
- **Runtime Verification**: Verification of end-to-end traversal is partially blocked due to missing local Docker infrastructure for PostgreSQL/pgvector and Neo4j. Tests utilize `unittest.mock` for component orchestration validation.

## Known Limitations
- Pure graph traversal (finding paths where no explicit vector text hits) still relies heavily on `query_understanding` parsing logic, which currently defaults safely to Vector fallback if unclear.

## Phase 6 Handoff
Phase 5 operates purely as functional orchestration. Phase 6 may introduce autonomous autonomous agents (Supervisor, Researcher) which can plug directly into `CIRANGraphService.invoke()` as a robust capability tool.
