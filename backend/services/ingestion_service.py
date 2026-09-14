import logging
from datetime import datetime, timezone
import uuid
from typing import Dict, Any, List

from sqlalchemy.orm import Session
from models.sql_models import RawRecord, Entity as SQLEntity, DocumentChunk
from services.document_parser import DocumentParser
from services.nlp_extractor import NLPExtractor
from services.identity_resolver import IdentityResolver
from services.chunking_service import ChunkingService
from services.embedding_service import EmbeddingService

class IngestionService:
    def __init__(self, db: Session, neo4j_session):
        self.db = db
        self.neo4j_session = neo4j_session
        self.extractor = NLPExtractor()
        self.resolver = IdentityResolver()
        self.chunker = ChunkingService(chunk_size=500, overlap=50)
        self.embedder = EmbeddingService()

    def process_document(self, filename: str, content: bytes, mime_type: str) -> Dict[str, Any]:
        """
        Main orchestration flow for Phase 2 data ingestion with Phase 4 Chunking/Embedding.
        """
        record_id = f"DOC-{uuid.uuid4().hex[:8].upper()}"
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # 1. Init RawRecord in PROCESSING state
        raw_record = RawRecord(
            id=record_id,
            type="document_upload",
            timestamp=timestamp,
            source_system="CIRAN_INGESTION",
            content={
                "filename": filename,
                "mime_type": mime_type,
                "status": "PROCESSING",
                "text_content": ""
            }
        )
        self.db.add(raw_record)
        self.db.commit()
        
        try:
            # 2. Extract Text
            text_content = DocumentParser.parse_file(filename, content, mime_type)
            raw_record.content["text_content"] = text_content
            self.db.commit()
            
            # 3. Extract NLP Entities & Relationships
            extraction_result = self.extractor.extract(text_content, record_id)
            if not extraction_result:
                raise ValueError("NLP Extraction returned no results or failed.")
                
            raw_entities = extraction_result.get("entities", [])
            raw_relationships = extraction_result.get("relationships", [])
            
            # 4. Entity Resolution & Postgres Persistence
            resolved_entities: Dict[str, SQLEntity] = {}
            val_to_id_map: Dict[str, str] = {}
            
            for ent in raw_entities:
                label = ent.get("value", "")
                ent_type = ent.get("type", "unknown")
                confidence = ent.get("confidence", 50)
                
                resolved_id = self.resolver.resolve_entity(label, ent_type, self.db)
                val_to_id_map[label] = resolved_id
                
                if resolved_id not in resolved_entities:
                    existing = self.db.query(SQLEntity).filter(SQLEntity.id == resolved_id).first()
                    if not existing:
                        new_ent = SQLEntity(
                            id=resolved_id,
                            type=ent_type,
                            label=label,
                            subtitle=f"{ent_type.capitalize()} record",
                            attributes=[{"label": "Confidence", "value": str(confidence)}],
                            cases=[],
                            priorityFactors=[]
                        )
                        self.db.add(new_ent)
                        resolved_entities[resolved_id] = new_ent
            
            self.db.commit() 
            
            # 5. Neo4j Persistence
            for resolved_id, ent in resolved_entities.items():
                label_cap = ent.type.capitalize()
                query = f"MERGE (n:{label_cap} {{id: $id}}) SET n.label = $label"
                self.neo4j_session.run(query, id=resolved_id, label=ent.label)
                
            inserted_rels = 0
            for rel in raw_relationships:
                source_val = rel.get("source")
                target_val = rel.get("target")
                rel_type = rel.get("type", "unknown").upper().replace(" ", "_")
                confidence = rel.get("confidence", 50)
                
                source_id = val_to_id_map.get(source_val)
                target_id = val_to_id_map.get(target_val)
                
                if source_id and target_id:
                    query = f"""
                    MATCH (source {{id: $source_id}})
                    MATCH (target {{id: $target_id}})
                    MERGE (source)-[r:{rel_type}]->(target)
                    SET r.sourceRecord = $sourceRecord,
                        r.confidence = $confidence,
                        r.timestamp = $timestamp
                    """
                    self.neo4j_session.run(
                        query,
                        source_id=source_id,
                        target_id=target_id,
                        sourceRecord=record_id,
                        confidence=confidence,
                        timestamp=timestamp
                    )
                    inserted_rels += 1

            # 6. Chunking and Embedding
            chunks = self.chunker.chunk_text(text_content)
            embeddings = self.embedder.embed_texts(chunks)
            chunks_saved = 0
            
            if embeddings and len(embeddings) == len(chunks):
                for idx, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
                    chunk_id = f"{record_id}-C{idx}"
                    doc_chunk = DocumentChunk(
                        id=chunk_id,
                        record_id=record_id,
                        chunk_index=idx,
                        text_content=chunk_text,
                        embedding=embedding,
                        timestamp=timestamp
                    )
                    self.db.add(doc_chunk)
                self.db.commit()
                chunks_saved = len(chunks)
                raw_record.content["status"] = "SUCCESS"
            else:
                logging.warning(f"Embedding failed for {record_id}, saving chunks without embeddings or marking degraded.")
                raw_record.content["status"] = "SUCCESS_NO_VECTOR"
                self.db.commit()

            return {
                "status": "success",
                "record_id": record_id,
                "entities_extracted": len(resolved_entities),
                "relationships_extracted": inserted_rels,
                "chunks_saved": chunks_saved
            }
            
        except Exception as e:
            logging.error(f"Ingestion failed for {record_id}: {e}")
            raw_record.content["status"] = "FAILED"
            raw_record.content["error"] = str(e)
            self.db.commit()
            return {
                "status": "failed",
                "record_id": record_id,
                "error": str(e)
            }
