import contextlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import entities, network, cases, alerts, patterns, cross_case, evidence, copilot, reports, ingestion, kpis, timeline, upload

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # auto-load mock data on startup
    from api.routes.ingestion import load_data
    try:
        load_data()
        print("Mock data loaded successfully on startup.")
    except Exception as e:
        print(f"Error loading initial mock data: {e}")
    yield

app = FastAPI(
    title="CIRAN Intelligence API",
    description="Phase 2 Backend for Criminal Intelligence & Relationship Analysis Network",
    version="2.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(entities.router, prefix="/api/entities", tags=["Entities"])
app.include_router(network.router, prefix="/api/network", tags=["Network"])
app.include_router(cases.router, prefix="/api/cases", tags=["Cases"])
app.include_router(alerts.router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(patterns.router, prefix="/api/patterns", tags=["Patterns"])
app.include_router(cross_case.router, prefix="/api/cross-case", tags=["Cross Case"])
app.include_router(evidence.router, prefix="/api/evidence", tags=["Evidence"])
app.include_router(copilot.router, prefix="/api/copilot", tags=["Copilot"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])
app.include_router(ingestion.router, prefix="/api/ingestion", tags=["Ingestion"])
app.include_router(kpis.router, prefix="/api/kpis", tags=["KPIs"])
app.include_router(timeline.router, prefix="/api/timeline", tags=["Timeline"])
app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "CIRAN Intelligence Engine Phase 1"}
