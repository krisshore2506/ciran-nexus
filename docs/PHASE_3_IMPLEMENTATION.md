# Phase 3 Implementation: Neo4j Graph Intelligence Layer

## Overview
Phase 3 transforms the CIRAN graph architecture from an in-memory Python implementation (BFS traversals) to a robust, Neo4j-native graph intelligence layer utilizing parameterized Cypher queries. PostgreSQL remains the source of truth for entities, while Neo4j becomes the exclusive engine for network routing, pathfinding, and graph operations.

## Architecture
The new graph intelligence stack is implemented via the `Neo4jGraphService`.
- **FastAPI Endpoints**: `backend/api/routes/network.py`
- **Graph Service**: `backend/services/neo4j_graph_service.py`
- **Legacy Service Migration**: `backend/services/graph_intelligence.py` now proxies shortest path and metrics calls to Neo4j.

**Data Flow**:
`Client Request` → `FastAPI` → `Neo4jGraphService` → `Neo4j Python Driver` (Parameterized Cypher) → `Neo4j Graph Database`

## Neo4j Schema
**Nodes**: Identical `id` matching PostgreSQL Entity IDs.
- `Person`, `Phone`, `Vehicle`, `Account`, `Location`, `Case`

**Relationships**: Generated during Phase 2 parsing.
- `COMMUNICATION`, `VEHICLE`, `LOCATION`, `CASE_ASSOCIATION`, `FINANCIAL`
- Properties: `sourceRecord`, `confidence`, `timestamp`

## Constraints
Unique ID constraints are automatically verified/created by `Neo4jGraphService.create_constraints()`. This protects against duplicate nodes across all entity categories.

## Graph Service Capabilities (Cypher Strategy)
All Cypher queries are strictly parameterized to prevent injection.

1. **Direct Neighbors (`get_direct_neighbors`)**: Retrieves all nodes directly connected (1 hop) from the target entity.
2. **Multi-Hop Traversal (`get_multi_hop_network`)**: Bounded depth traversal (`max_depth` restricted between 1 and 5) returning a de-duplicated map of nodes and edges.
3. **Shortest Path (`find_shortest_path`)**: Utilizes Neo4j native `shortestPath` function up to a maximum defined boundary (e.g., 6 hops) to find the most direct link between two entities.
4. **Common Connections (`get_common_connections`)**: Identifies shared nodes situated exactly 1 hop between two provided entities.
5. **Case Network (`get_case_network`)**: Queries directly off a `Case` node for its local network scope.
6. **Metrics (`get_graph_metrics`)**: Uses Neo4j aggregations (`count`, `sum`) to calculate degree centrality and linked case frequency.

## API Endpoints
- `GET /api/network`: Exposes the entire graph (safety-limited).
- `GET /api/network/entity/{entity_id}/network?max_depth={d}`: Returns bounded subgraph.
- `GET /api/network/shortest-path?source={src}&target={tgt}&max_depth={d}`: Calculates pathing.
- `GET /api/network/common-connections?source={src}&target={tgt}`: Shared neighboring entities.
- `GET /api/network/case/{case_id}/network`: Dedicated case network scope.
- `GET /api/network/metrics/{entity_id}`: Graph metadata extraction.

## Security
- **No string formatting**: All dynamic variables passed to Neo4j are injected as parameter bindings.
- **Bounds enforcement**: All iterative traversals check strict depth boundaries defined at the Python service layer.
- **Pagination/Limit**: Global network exposure is capped tightly.

## State.py Migration Status
- **Network API**: Fully decoupled from `state.py`.
- **Neo4jGraphService**: Operates independently.
- **GraphIntelligence**: Decoupled from `RelationshipEngine` and legacy BFS.
- **Legacy Components**: Features like `CopilotRetrievalService` and `CorrelationEngine` currently still rely on the legacy Python dictionary relationships due to scope bounding. These will be migrated in subsequent analytics phases.

## Testing & Runtime Verification
- Integration tests written in `tests/test_neo4j_graph.py` covering standard and bounds-exceeded parameters.
- **Runtime Verification**: BLOCKED in current environment due to missing Docker daemon (`docker: The term 'docker' is not recognized`). Static verification and service compilation verified.

## Known Limitations
- The frontend visualization component (`NetworkGraph`) remains static with hardcoded layouts. Upgrading the UI is deferred to Phase 4+.
