from typing import List, Dict, Optional, Tuple, Literal
from models.domain import Entity

IntentType = Literal[
    "ENTITY_CONTEXT",
    "RISK_EXPLANATION",
    "CROSS_CASE_LINK",
    "TIMELINE",
    "SUMMARIZE_CASE",
    "UNKNOWN"
]

class QueryParser:
    def __init__(self):
        # Basic keyword maps for intent classification
        self.intent_keywords = {
            "RISK_EXPLANATION": ["risk", "flagged", "alert", "dangerous", "priority"],
            "CROSS_CASE_LINK": ["connects case", "link between", "between case", "shared case", "cross-case", "what connects"],
            "TIMELINE": ["timeline", "when", "events", "time", "date", "chronological"],
            "SUMMARIZE_CASE": ["summarize", "summary", "report", "overview"],
            "ENTITY_CONTEXT": ["who is", "connections", "show", "transaction", "relations", "relationship"]
        }
        
    def parse_query(self, query: str, state_entities: List[Entity]) -> Tuple[IntentType, List[Entity]]:
        """
        Parses natural language query to determine intent and extract entities present in the graph.
        Returns: Tuple of (Intent, list of matched Entity objects)
        """
        q = query.lower()
        
        # 1. Intent Classification
        intent: IntentType = "UNKNOWN"
        best_score = 0
        
        for i_type, keywords in self.intent_keywords.items():
            score = sum(1 for kw in keywords if kw in q)
            if score > best_score:
                best_score = score
                intent = i_type # type: ignore
                
        # Fallback heuristic: if no explicit keyword but looks like a question about a specific entity/case
        if intent == "UNKNOWN" and ("what" in q or "who" in q or "show" in q):
            intent = "ENTITY_CONTEXT"
            
        # 2. Entity Extraction (Grounded only to existing state entities)
        extracted = []
        for ent in state_entities:
            # check exact ID match first
            if ent.id.lower() in q:
                extracted.append(ent)
            # check label match if label is substantial
            elif len(ent.label) > 3 and ent.label.lower() in q:
                if ent not in extracted:
                    extracted.append(ent)
                    
        # Heuristic fix for "SUMMARIZE_CASE" if a case is extracted
        if intent == "SUMMARIZE_CASE":
            cases_found = [e for e in extracted if e.type == "case"]
            if not cases_found:
                intent = "UNKNOWN" # Cannot summarize case if no case found
        
        return intent, extracted
