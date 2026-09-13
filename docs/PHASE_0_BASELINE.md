# PHASE 0: SYSTEM BASELINE

## 1. Current project version/state
- **Status**: Stable SIH Prototype (Mock Data & In-Memory State)
- **Branch**: `ciran-upgrade`
- **Git Hash**: Checked out from `main` (Latest commit: `chore: baseline SIH prototype before CIRAN upgrade`)

## 2. How to start frontend
- **Command**: `npm run dev` or `bun dev` (from `c:\PROJECTS\ciran`)
- **Note**: Currently fails in local environment due to missing `npm` in PATH. The project also uses `bun` (as indicated by `bun.lock`).

## 3. How to start backend
- **Command**: `.\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000` (from `c:\PROJECTS\ciran\backend`)
- **Note**: Currently fails in local environment due to a broken virtual environment (`C:\Python314\python.exe` Access is denied).

## 4. Environment variables required
- **Backend**: `LLM_PROVIDER`, `LLM_API_KEY` (Optional for local test, required for Copilot AI).

## 5. Available API endpoints
- **Entities**: `GET /api/entities`, `GET /api/entities/{id}`
- **Network**: `GET /api/network`
- **Cases**: `GET /api/cases`, `GET /api/cases/{id}`
- **Alerts**: `GET /api/alerts`
- **Patterns**: `GET /api/patterns`
- **Cross Case**: `GET /api/cross-case`
- **Evidence**: `GET /api/evidence`
- **Copilot**: `POST /api/copilot/query`
- **Ingestion**: `POST /api/ingestion/load`
- **Reports**: `GET /api/reports`
- **KPIs**: `GET /api/kpis`
- **Timeline**: `GET /api/timeline`

## 6. Known working features
- Mock data ingestion pipeline.
- Global in-memory state management.
- Backend API endpoints outputting mock data.
- Frontend UI components (Dashboard, Network SVG Graph, Copilot chat UI).

## 7. Known broken features
- **Local Startup**: Fails due to environment missing `npm` and broken Python virtual environment.
- **Authentication**: Bypassed; no actual security.
- **Data Persistence**: Lost on backend restart.

## 8. Known mock-data dependencies
- `synthetic_data.json` inside backend.
- `ciran-data.ts` in frontend `lib/`.

## 9. Known technical debt
- Backend `state.py` acting as an in-memory global database.
- Synchronous CPU-heavy processing loops during data ingestion.
- Frontend graph uses hardcoded node SVG positions instead of a dynamic layout engine.
