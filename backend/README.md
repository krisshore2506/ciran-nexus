# CIRAN Intelligence Engine Phase 1 Backend

This is the modular Python/FastAPI backend for the CIRAN (Criminal Intelligence & Relationship Analysis Network) system.

## Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload --port 8000
```

## Running Tests

Run the test suite using pytest:

```bash
pytest tests/
```

## Initializing Data

The system uses an in-memory graph for Phase 1. You must load the synthetic test dataset before querying the APIs:

```bash
curl -X POST http://localhost:8000/api/ingestion/load
```

## Integrating with the Frontend

To connect the existing React/Vite frontend to this backend, update the frontend's API calls to point to `http://localhost:8000/api/...` instead of the local mock services.
