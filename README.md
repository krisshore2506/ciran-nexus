# CIRAN (Criminal Intelligence & Relationship Analysis Network)

Welcome to the CIRAN documentation.

CIRAN is a multi-agent intelligence prototype designed to process raw documents, extract entities and relationships, embed them into a pgvector store, load them into a Neo4j graph, and expose them through a React dashboard and a LangGraph Copilot.

## Architecture

Data Flow:
Data → PostgreSQL → Neo4j → pgvector → RAG → LangGraph → Multi-Agent → FastAPI → Dashboard

## Features

- **Entity Intelligence**: Deterministic entity extraction and identity resolution.
- **Network Analysis**: Multi-hop graph traversal and visualization.
- **Evidence Retrieval**: RAG-based search with source traceability.
- **Cross-case Correlation**: Deterministic linking between separated case files.
- **Explainable Risk Indicators**: Transparent scoring and rule-based risk factors.
- **Multi-agent Copilot**: LangGraph orchestrated conversational assistant.
- **Evidence Traceability**: Strict audit logs pinning generated insights back to explicit records.

## Setup & Deployment

**Prerequisites:**
- Docker and Docker Compose
- Node.js and npm
- Python 3.10+
- OpenAI API Key (or other LLM Provider for vector embeddings)

**Configuration:**
1. Copy `.env.example` to `.env`.
2. Configure `LLM_API_KEY` with your provider key.
3. Keep `VITE_USE_MOCK_DATA=false`.

**Database Initialization (Requires Docker):**
```bash
docker compose up -d
```
*(Verify PostgreSQL and Neo4j are running on ports 5432 and 7474)*

**Backend Setup (Requires Python):**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python scripts/seed.py    # Run data ingestion seed
uvicorn main:app --reload
```

**Frontend Setup (Requires Node):**
```bash
npm install
npm run dev
```

## Final Project Demo Flow

Recommended demonstration steps:
1. **Dashboard**: Show high-level system metrics and recent alerts.
2. **Entity Search**: Search for a specific entity profile across the database.
3. **Network Graph**: Explore the exact Neo4j structural graph representing the intelligence connections.
4. **Case Details**: View ingested case documents and parsed intelligence.
5. **Evidence**: Review the audit trail linking insights back to specific uploaded documents.
6. **Cross-case Correlation**: Navigate to see deterministic overlap between disparate cases.
7. **Risk Indicators**: Observe how transparent scoring calculates network threat levels.
8. **Copilot Query**: Ask the Copilot a complex question.
9. **Show Source References**: Click through the exact sources the Copilot cites in its response.
10. **Multi-agent Architecture**: Explain how the Copilot routes the query to Evidence, Network, Correlation, and Risk agents concurrently.

## Legal / Analytical Scope

The system is an intelligence-analysis prototype. It provides **associations, correlations, network connections, risk indicators, and supporting evidence**.
It does **NOT claim guilt, criminal certainty, conviction, probability of guilt, or automatic criminal classification.**
