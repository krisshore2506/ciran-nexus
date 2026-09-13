import os
import sys
import json
from dotenv import load_dotenv

# Add backend dir to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from config.db import engine, SessionLocal, Base
from config.neo4j import neo4j_driver
from models.sql_models import RawRecord, Entity, Alert, TimelineEvent
from ingestion.loaders import load_json
from ingestion.normalizer import normalize_records
from services.entity_extraction import EntityExtractionService
from services.relationship_engine import RelationshipEngine

def seed_database():
    print("Initializing Database Schemas...")
    Base.metadata.drop_all(bind=engine) # Clear existing for idempotent seed
    Base.metadata.create_all(bind=engine)
    
    print("Loading synthetic_data.json...")
    raw_data_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample", "synthetic_data.json")
    if not os.path.exists(raw_data_path):
        print(f"Error: {raw_data_path} not found.")
        return

    raw_records = load_json(raw_data_path)
    normalized = normalize_records(raw_records)
    
    extractor = EntityExtractionService()
    rel_engine = RelationshipEngine()
    
    print("Processing Records...")
    for rec in normalized:
        extracted = extractor.process_record(rec)
        rel_engine.process_record(rec, extracted)
        
    entities = list(extractor.entities_store.values())
    relations = rel_engine.get_relations()
    
    print(f"Extracted {len(entities)} Entities and {len(relations)} Relationships.")
    
    # 1. Seed PostgreSQL
    print("Seeding PostgreSQL...")
    db = SessionLocal()
    try:
        # Seed RawRecords
        for raw in raw_records:
            record_db = RawRecord(
                id=raw["id"],
                type=raw["type"],
                timestamp=raw["timestamp"],
                source_system=raw["source_system"],
                content=raw.get("content", {})
            )
            db.merge(record_db)
            
        # Seed Entities
        for ent in entities:
            ent_db = Entity(
                id=ent.id,
                type=ent.type,
                label=ent.label,
                subtitle=ent.subtitle,
                priority=ent.priority,
                priorityBand=ent.priorityBand,
                cases=ent.cases,
                attributes=[attr.model_dump() for attr in (ent.attributes or [])],
                relationships=ent.relationships,
                recentEvents=ent.recentEvents,
                priorityFactors=[pf.model_dump() for pf in (ent.priorityFactors or [])]
            )
            db.merge(ent_db)
            
        db.commit()
        print("PostgreSQL Seeding Complete.")
    except Exception as e:
        db.rollback()
        print(f"PostgreSQL Seeding Failed: {e}")
    finally:
        db.close()
        
    # 2. Seed Neo4j
    print("Seeding Neo4j...")
    neo4j_driver.connect()
    session = neo4j_driver.get_session()
    try:
        # Clear existing graph (for idempotent seed)
        session.run("MATCH (n) DETACH DELETE n")
        
        # Seed Nodes
        for ent in entities:
            # Map types to capitalized labels (e.g. person -> Person)
            label = ent.type.capitalize()
            query = f"MERGE (n:{label} {{id: $id}}) SET n.label = $label"
            session.run(query, id=ent.id, label=ent.label)
            
        # Seed Relationships
        for rel in relations:
            # Cypher requires relationship types to be uppercase and underscores
            rel_type = rel.type.upper().replace(" ", "_")
            query = f"""
            MATCH (source {{id: $source_id}})
            MATCH (target {{id: $target_id}})
            MERGE (source)-[r:{rel_type}]->(target)
            SET r.sourceRecord = $sourceRecord,
                r.confidence = $confidence,
                r.timestamp = $timestamp
            """
            session.run(query, 
                       source_id=rel.source, 
                       target_id=rel.target,
                       sourceRecord=rel.sourceRecord,
                       confidence=rel.confidence,
                       timestamp=rel.timestamp)
            
        print("Neo4j Seeding Complete.")
    except Exception as e:
        print(f"Neo4j Seeding Failed: {e}")
    finally:
        session.close()
        neo4j_driver.close()

if __name__ == "__main__":
    seed_database()
