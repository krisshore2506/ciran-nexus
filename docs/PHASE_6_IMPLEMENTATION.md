# Phase 6 Implementation: Multi-Agent Intelligence Layer

## Objective
Extend the LangGraph orchestration framework (Phase 5) into a robust Multi-Agent Intelligence System. Specialized agents now handle Evidence, Network, Correlation, and Risk scoring, governed by a Supervisor agent, maintaining sequential execution for determinism and simplicity.

## Architecture

1. **State Modifications**:
   - `CIRANGraphState` is upgraded to store multi-agent results (`evidence_result`, `network_result`, etc.).
   - `requested_capabilities` tracks the dynamic agent execution pipeline dictated by the Supervisor.
   - `fused_context` and `validation_status` orchestrate grounded generation.

2. **Specialized Agents**:
   - **SupervisorAgent**: Uses heuristic intent mapping to trigger appropriate intelligence nodes. Does NOT access the DB or LLMs directly.
   - **EvidenceAgent**: Wraps `VectorSearchService`. Discovers grounded documents.
   - **NetworkAgent**: Wraps `ContextBuilder` and `Neo4jGraphService` to pull node neighborhoods.
   - **CorrelationAgent**: Detects intersecting network components across different cases. Refuses unsupported correlations.
   - **RiskAgent**: Scores risk using explainable network factors (density, overlapping cases) while preventing spurious guilt attributions.
   - **EvidenceValidator**: Blocks ungrounded assertions from reaching the Response Generator, routing them to `safe_response`.

## Execution Flow
The LangGraph pipeline evaluates capabilities dynamically and sequentially:
`Supervisor` -> `Evidence` (opt) -> `Network` (opt) -> `Correlation` (opt) -> `Risk` (opt) -> `Aggregator` -> `Validator` -> `Generator`/`SafeResponse`

## API Integration
Phase 6 maps directly into the existing `ciran_graph.invoke()` interface without breaking `CopilotResponse` boundaries, ensuring complete backward compatibility with Phase 5 endpoints.

## Known Limitations
- Pure parallelism was omitted to keep state management deterministic for a 3rd-year project.
- Mocking was utilized for multi-agent logic tests due to environmental restrictions on local PostgreSQL/Neo4j execution.

## Phase 7 Handoff
The Multi-Agent architecture is now stabilized. Phase 7 can introduce UI components for visualizing the agents' thought processes, or deploy the solution.
