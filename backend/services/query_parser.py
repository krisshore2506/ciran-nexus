import re
from typing import List, Dict, Optional, Tuple, Literal, Any
from models.domain import Entity, StructuredQuery, ChatMessage

class QueryParser:
    def __init__(self):
        self.intent_keywords = {
            "RISK_EXPLANATION": [
                "risk", "flagged", "alert", "dangerous", "priority", "why", 
                "suspicious", "explain the risk", "explain"
            ],
            "CROSS_CASE_LINK": [
                "connects case", "link between", "between case", "shared case", 
                "cross-case", "what connects", "cases connected", "other investigations",
                "find cases involving", "cases involving", "appear in other", "compare"
            ],
            "TIMELINE": [
                "timeline", "when", "events", "time", "date", "chronological", 
                "happened", "recently", "days", "recent activity", "what changed"
            ],
            "SUMMARIZE_CASE": [
                "summarize", "summary", "report", "overview", "key findings",
                "brief me on", "what do we know about"
            ],
            "ENTITY_CONTEXT": [
                "who is", "connections", "show", "transaction", "relations", 
                "relationship", "connected to", "network", "associates",
                "linked to", "tell me about", "associated with"
            ]
        }
        
    def _extract_time_range(self, query: str) -> Optional[str]:
        if re.search(r'\b(today)\b', query): return "today"
        if re.search(r'\b(yesterday)\b', query): return "yesterday"
        if re.search(r'\b(recently|recent)\b', query): return "recently"
        if re.search(r'\b(this month)\b', query): return "this_month"
        if re.search(r'\b(last month|past month)\b', query): return "last_month"
        if re.search(r'\b(past week|last week)\b', query): return "last_week"
        match = re.search(r'last (\d+) days?', query)
        if match: return f"{match.group(1)}_days"
        return None
        
    def parse_query(self, query: str, state_entities: List[Entity], history: Optional[List[Any]] = None) -> StructuredQuery:
        q = query.lower()
        confidence = 0.0
        ambiguous = False
        
        # 1. Intent Classification
        intent = "UNKNOWN"
        best_score = 0
        for i_type, keywords in self.intent_keywords.items():
            score = sum(1 for kw in keywords if kw in q)
            if score > best_score:
                best_score = score
                intent = i_type
                
        if best_score >= 2: confidence += 0.5
        elif best_score == 1: confidence += 0.3
            
        if intent == "UNKNOWN" and any(w in q for w in ["what", "who", "show"]):
            intent = "ENTITY_CONTEXT"
            confidence += 0.1
            
        # 2. Entity Extraction
        final_entities = []
        matched_words = set()
        
        for ent in state_entities:
            id_lower = ent.id.lower()
            label_lower = ent.label.lower()
            if id_lower in q:
                if ent not in final_entities: final_entities.append(ent)
                matched_words.update(id_lower.split())
            elif len(label_lower) > 3 and label_lower in q:
                if ent not in final_entities: final_entities.append(ent)
                matched_words.update(label_lower.split())
                
        if not final_entities:
            word_to_entities = {}
            for ent in state_entities:
                label_lower = ent.label.lower()
                parts = label_lower.split()
                for part in parts:
                    if len(part) > 3 and part not in matched_words and re.search(rf'\b{re.escape(part)}\b', q):
                        if part not in word_to_entities:
                            word_to_entities[part] = []
                        word_to_entities[part].append(ent)
                        
            for word, ents in word_to_entities.items():
                if len(ents) > 1: ambiguous = True
                for e in ents:
                    if e not in final_entities: final_entities.append(e)
                    
        if final_entities: confidence += 0.4
        if ambiguous: confidence -= 0.3

        # 3. Coreference Resolution
        if not final_entities and history:
            pronouns = ["he", "him", "she", "her", "they", "this", "it", "his", "their"]
            if any(re.search(rf'\b{p}\b', q) for p in pronouns):
                for msg in reversed(history):
                    hist_text = msg.content.lower() if hasattr(msg, "content") else (msg.get("content", "").lower() if isinstance(msg, dict) else "")
                    for ent in state_entities:
                        if ent.id.lower() in hist_text or (len(ent.label) > 3 and ent.label.lower() in hist_text):
                            if ent not in final_entities: final_entities.append(ent)
                    if final_entities:
                        confidence += 0.2
                        break
                        
        if intent == "SUMMARIZE_CASE":
            cases_found = [e for e in final_entities if e.type == "case"]
            if not cases_found:
                intent = "UNKNOWN"
                
        time_range = self._extract_time_range(q)
        if time_range: confidence += 0.1
            
        if not final_entities and intent != "UNKNOWN": confidence -= 0.4
            
        confidence = max(0.0, min(1.0, round(confidence, 2)))
        
        return StructuredQuery(
            intent=intent,
            entities=[e.id for e in final_entities],
            time_range=time_range,
            ambiguous=ambiguous,
            confidence=confidence
        )
