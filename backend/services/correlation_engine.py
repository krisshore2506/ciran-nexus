from typing import List, Dict, Set, Tuple
from models.domain import Entity, CrossCaseLink, SharedAttribute
from services.relationship_engine import RelationshipEngine
from services.graph_intelligence import GraphIntelligenceService

class CorrelationEngine:
    def __init__(self, relationship_engine: RelationshipEngine, graph_intelligence: GraphIntelligenceService):
        self.relationship_engine = relationship_engine
        self.graph_intelligence = graph_intelligence
        
    def find_cross_case_links(self, entities: List[Entity]) -> List[Tuple[CrossCaseLink, List[str]]]:
        cases = [e for e in entities if e.type == "case"]
        other_entities = [e for e in entities if e.type != "case"]
        
        links = []
        
        # 1. Direct Shared Entity (Phase 1 logic but with explicit provenance filtering)
        entity_to_cases: Dict[str, Set[str]] = {}
        for ent in other_entities:
            neighbors = self.relationship_engine.get_neighbors(ent.id)
            case_ids = {r.target if r.target.startswith("CASE") else r.source for r in neighbors if "CASE" in r.target or "CASE" in r.source}
            if len(case_ids) > 1:
                entity_to_cases[ent.id] = case_ids
                
        # Group shared entities by case combinations
        case_pairs_to_entities: Dict[frozenset, List[Entity]] = {}
        for ent_id, c_ids in entity_to_cases.items():
            key = frozenset(c_ids)
            if key not in case_pairs_to_entities:
                case_pairs_to_entities[key] = []
            
            ent = next(e for e in entities if e.id == ent_id)
            case_pairs_to_entities[key].append(ent)
            
        for case_set, shared_ents in case_pairs_to_entities.items():
            if len(case_set) < 2:
                continue
                
            cases_list = list(case_set)
            shared_attrs = [SharedAttribute(type=f"Shared {e.type.capitalize()}", value=e.label) for e in shared_ents]
            
            path = [cases_list[0], shared_ents[0].label, cases_list[1]]
            summary = f"Detected {len(shared_ents)} shared entities connecting {len(cases_list)} independent investigation records."
            
            # Find exact source records
            source_ids = set()
            for ent in shared_ents:
                neighbors = self.relationship_engine.get_neighbors(ent.id)
                for r in neighbors:
                    if (r.target in case_set or r.source in case_set) and r.sourceRecord != "RESOLUTION_ENGINE":
                        source_ids.add(r.sourceRecord)
            
            link = CrossCaseLink(
                cases=cases_list,
                shared=shared_attrs,
                path=path,
                confidence=70 + (len(shared_ents) * 5),
                evidence=[],
                summary=summary
            )
            links.append((link, list(source_ids)))
            
        # 2. Multi-hop Case Correlation (Phase 3 enhancement)
        # Find path between cases up to depth 3
        for i, c1 in enumerate(cases):
            for c2 in cases[i+1:]:
                # Only if not already directly linked
                if frozenset([c1.id, c2.id]) in case_pairs_to_entities:
                    continue
                    
                path_info = self.graph_intelligence.find_shortest_path(c1.id, c2.id, max_depth=3)
                if path_info:
                    path_nodes, ev = path_info
                    if len(path_nodes) > 3: # multi-hop
                        path_labels = [next((e.label for e in entities if e.id == nid), nid) for nid in path_nodes]
                        link = CrossCaseLink(
                            cases=[c1.id, c2.id],
                            shared=[],
                            path=path_labels,
                            confidence=50,
                            evidence=[],
                            summary=f"Discovered indirect multi-hop link between {c1.id} and {c2.id} spanning {len(path_nodes)-1} connections."
                        )
                        links.append((link, ev))
            
        return links
