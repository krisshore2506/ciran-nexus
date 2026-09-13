# Phase 1: Implementation Details

## Infrastructure Setup

### Prerequisites
- Docker & Docker Compose
- Node.js (for frontend)
- Python 3.10+ (for backend)

### Starting Databases
Run the following command in the project root to start PostgreSQL and Neo4j:
```bash
docker compose up -d
```
- **PostgreSQL**: Accessible at `localhost:5432`
- **Neo4j**: Accessible at `localhost:7474` (HTTP) and `localhost:7687` (Bolt)

### Environment Variables
Configure the following in the backend `.env` file (defaults match docker-compose):
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgrespassword
POSTGRES_DB=ciran_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=neo4jpassword
```

## Database Seeding
To populate PostgreSQL and Neo4j with the mock data from `synthetic_data.json`, run:
```bash
cd backend
python -m scripts.seed
```
This script acts idempotently by clearing the database and graph before inserting.

## Starting the Application

### Backend
```bash
cd backend
# Activate virtual environment
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
npm run dev
```

## API Testing
You can test the migrated endpoints via curl or Swagger UI (`http://localhost:8000/docs`):

1. **Entities**: `curl http://localhost:8000/api/entities`
2. **Network**: `curl http://localhost:8000/api/network`
3. **Cases**: `curl http://localhost:8000/api/cases`
4. **Entity Network**: `curl http://localhost:8000/api/entities/P-RAVI/network`

## Status of `state.py`
`state.py` has been retained to support legacy services (e.g., Copilot, Graph Intelligence, Risk Engine) which have not yet been migrated. The read APIs (`entities`, `cases`, `network`) have been migrated to the new persistent databases.

## Known Limitations
- The virtual environment and `npm` paths were broken in the current development environment, restricting local integration testing.
- `state.py` still drives ingestion and analytics for unmigrated components.
- `pgvector` has not been introduced yet.
