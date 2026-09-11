from typing import List, Any, Optional
from collections import deque
from models.domain import Entity, StructuredQuery, RetrievalResult, Relation

class CopilotRetrievalService:
    def __init__(self):
        self.max_depth = 3
        self.max_nodes = 50

    def retrieve(self, query: StructuredQuery, state: Any, extracted_entities: List[Entity]) -> RetrievalResult:
        result = RetrievalResult()
        
        if not extracted_entities and query.intent != "UNKNOWN":
            result.retrieval_notes.append("No matching entity was found in the available CIRAN records.")
            return result
            
        if query.intent == "ENTITY_CONTEXT":
            if len(extracted_entities) == 1:
                self._retrieve_single_entity_context(extracted_entities[0], state, result)
            elif len(extracted_entities) >= 2:
                self._retrieve_multi_entity_graph(extracted_entities[0], extracted_entities[1], state, result)
        elif query.intent == "RISK_EXPLANATION":
            self._retrieve_risk(extracted_entities, state, result)
        elif query.intent == "CROSS_CASE_LINK":
            self._retrieve_cross_case(extracted_entities, state, result)
        elif query.intent == "TIMELINE":
            self._retrieve_timeline(extracted_entities, state, query.time_range, result)
        elif query.intent == "SUMMARIZE_CASE":
            self._retrieve_case_summary(extracted_entities, state, result)
            
        return result

    def _retrieve_single_entity_context(self, entity: Entity, state: Any, result: RetrievalResult):
        neighbors = state.relationship_engine.get_neighbors(entity.id)
        real_neighbors = [n for n in neighbors if n.sourceRecord != "RESOLUTION_ENGINE"]
        
        if not real_neighbors:
            result.retrieval_notes.append("No related relationships were found for this entity in the available CIRAN records.")
            return
            
        result.relationships.extend(real_neighbors)
        result.evidence.extend([n.sourceRecord for n in real_neighbors if n.sourceRecord != "RESOLUTION_ENGINE"])

    def _retrieve_multi_entity_graph(self, src: Entity, tgt: Entity, state: Any, result: RetrievalResult):
        # 1. Direct check
        src_neighbors = state.relationship_engine.get_neighbors(src.id)
        direct_edges = [n for n in src_neighbors if (n.source == src.id and n.target == tgt.id) or (n.source == tgt.id and n.target == src.id)]
        
        if direct_edges:
            result.relationships.extend(direct_edges)
            result.paths.append(f"{src.label} -> {tgt.label}")
            result.retrieval_notes.append("DIRECT_CONNECTION")
            result.evidence.extend([e.sourceRecord for e in direct_edges if e.sourceRecord != "RESOLUTION_ENGINE"])
            return

        # 2. Shared case / entity check (depth 2 essentially)
        tgt_neighbors = state.relationship_engine.get_neighbors(tgt.id)
        src_conn = {n.target if n.source == src.id else n.source for n in src_neighbors}
        tgt_conn = {n.target if n.source == tgt.id else n.source for n in tgt_neighbors}
        intersection = src_conn.intersection(tgt_conn)
        
        if intersection:
            shared_id = list(intersection)[0]
            shared_ent = next((e for e in state.entities if e.id == shared_id), None)
            
            if shared_ent:
                # Get the edges connecting to this shared entity
                s_e = [n for n in src_neighbors if n.source == shared_id or n.target == shared_id]
                t_e = [n for n in tgt_neighbors if n.source == shared_id or n.target == shared_id]
                result.relationships.extend(s_e + t_e)
                
                if shared_ent.type == "case":
                    result.retrieval_notes.append(f"SHARED_CASE:{shared_ent.label}")
                    result.cases.append(shared_ent.id)
                else:
                    result.retrieval_notes.append(f"SHARED_ENTITY:{shared_ent.label}")
                
                result.paths.append(f"{src.label} -> {shared_ent.label} -> {tgt.label}")
                result.evidence.extend([e.sourceRecord for e in (s_e + t_e) if e.sourceRecord != "RESOLUTION_ENGINE"])
                return

        # 3. BFS for indirect path
        visited = {src.id: None}
        queue = deque([src.id])
        explored = 0
        target_found = False
        
        while queue and explored < self.max_nodes:
            curr = queue.popleft()
            if curr == tgt.id:
                target_found = True
                break
                
            explored += 1
            neighbors = state.relationship_engine.get_neighbors(curr)
            for n in neighbors:
                next_node = n.target if n.source == curr else n.source
                if next_node not in visited:
                    visited[next_node] = (curr, n) # store parent and edge
                    
                    path = self._build_path(visited, next_node, src.id)
                    if len(path) <= self.max_depth + 1:
                        queue.append(next_node)
                        
        if target_found:
            edges = []
            curr = tgt.id
            path_labels = [tgt.label]
            while curr != src.id:
                parent, edge = visited[curr]
                edges.append(edge)
                p_ent = next((e for e in state.entities if e.id == parent), None)
                if p_ent:
                    path_labels.insert(0, p_ent.label)
                else:
                    path_labels.insert(0, parent)
                curr = parent
                
            result.relationships.extend(edges)
            result.paths.append(" -> ".join(path_labels))
            result.retrieval_notes.append("INDIRECT_CONNECTION")
            result.evidence.extend([e.sourceRecord for e in edges if e.sourceRecord != "RESOLUTION_ENGINE"])
        else:
            result.retrieval_notes.append("No connection was found in the currently available CIRAN records.")

    def _build_path(self, visited: dict, end: str, start: str) -> list:
        path = [end]
        curr = end
        while curr != start and curr in visited and visited[curr] is not None:
            curr = visited[curr][0]
            path.append(curr)
        return path[::-1]

    def _retrieve_cross_case(self, entities: List[Entity], state: Any, result: RetrievalResult):
        for ent in entities:
            case_links = [l for l in getattr(state, "cross_case_links", []) if ent.id in l.cases]
            if case_links:
                for link in case_links:
                    if link.path:
                        result.paths.extend(link.path)
                    result.evidence.extend([ev for ev in link.evidence if ev != "RESOLUTION_ENGINE"])
            else:
                result.retrieval_notes.append(f"No cross-case links detected for {ent.label}.")
                
    def _retrieve_timeline(self, entities: List[Entity], state: Any, time_range: Optional[str], result: RetrievalResult):
        if time_range:
            result.retrieval_notes.append(f"NOTE: Time constraint '{time_range}' could not be dynamically applied from current records.")
            
        for ent in entities:
            patterns = [p for p in getattr(state, "patterns", []) if ent.id in p.entities and p.category == "Temporal Burst"]
            events = [e for e in getattr(state, "timeline", []) if ent.id in e.entities]
            
            result.patterns.extend(patterns)
            result.events.extend(events)
            
            for p in patterns:
                result.evidence.extend([ev for ev in p.evidence if ev != "RESOLUTION_ENGINE"])
            for e in events:
                if e.record != "RESOLUTION_ENGINE":
                    result.evidence.append(e.record)
                
            if not patterns and not events:
                result.retrieval_notes.append(f"No significant temporal patterns or events detected for {ent.label}.")

    def _retrieve_risk(self, entities: List[Entity], state: Any, result: RetrievalResult):
        for ent in entities:
            if not ent.priorityFactors:
                result.retrieval_notes.append(f"No documented risk factors in the current state for {ent.label}.")
            else:
                neighbors = state.relationship_engine.get_neighbors(ent.id)
                ev = [n.sourceRecord for n in neighbors if n.sourceRecord != "RESOLUTION_ENGINE"]
                result.evidence.extend(ev)
                
    def _retrieve_case_summary(self, entities: List[Entity], state: Any, result: RetrievalResult):
        for ent in entities:
            if ent.type != "case":
                result.retrieval_notes.append(f"Entity {ent.label} is not a case. Cannot summarize.")
                continue
                
            neighbors = state.relationship_engine.get_neighbors(ent.id)
            ev = [n.sourceRecord for n in neighbors if n.sourceRecord != "RESOLUTION_ENGINE"]
            
            if not ev:
                result.retrieval_notes.append(f"Insufficient evidence available in the connected CIRAN records for {ent.label}.")
            else:
                result.relationships.extend(neighbors)
                result.evidence.extend(ev)
