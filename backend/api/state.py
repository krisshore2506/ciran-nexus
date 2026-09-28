from typing import List, Dict
from models.domain import Entity, Relation, Alert, CrossCaseLink, EvidenceItem, TimelineEvent, PatternInsight
from services.entity_extraction import EntityExtractionService
from services.relationship_engine import RelationshipEngine
from services.correlation_engine import CorrelationEngine
from services.risk_engine import RiskEngine
from services.evidence_engine import EvidenceEngine
from services.report_generator import ReportGenerator
from services.entity_resolution import EntityResolutionService
from services.graph_intelligence import GraphIntelligenceService
from services.temporal_analysis import TemporalAnalysisService
from services.query_parser import QueryParser


class AppState:
    def __init__(self):
        self.entities: List[Entity] = []
        self.relations: List[Relation] = []
        self.alerts: List[Alert] = []
        self.cross_case_links: List[CrossCaseLink] = []
        self.evidence: List[EvidenceItem] = []
        self.timeline: List[TimelineEvent] = []
        self.patterns: List[PatternInsight] = []

        self.entity_service = EntityExtractionService()
        self.relationship_engine = RelationshipEngine()
        self.entity_resolution_service = EntityResolutionService(
            self.relationship_engine
        )
        self.graph_intelligence = GraphIntelligenceService(
            self.relationship_engine
        )
        self.temporal_analysis = TemporalAnalysisService(
            self.relationship_engine
        )
        self.correlation_engine = CorrelationEngine(
            self.relationship_engine,
            self.graph_intelligence
        )
        self.risk_engine = RiskEngine(self.relationship_engine)
        self.evidence_engine = EvidenceEngine()

        # LLMService is initialized by the DB-backed CIRAN graph flow.
        # Keeping it here causes CopilotRetrievalService to start without
        # required PostgreSQL and Neo4j sessions.
        self.query_parser = QueryParser()
        self.report_generator = ReportGenerator()


state = AppState()