import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.routes.ingestion import load_data, IngestionRequest
from api.state import state

def verify_phase3():
    # 1. Load Crime Data
    req_crime = IngestionRequest(
        dataset="crime",
        file_path=r"C:\PROJECTS\ciran\backend\data\real\archive1\crime_dataset_india.csv",
        max_rows=100
    )
    res_crime = load_data(req_crime)

    # 2. Load Email Data
    req_email = IngestionRequest(
        dataset="email",
        file_path=r"C:\Users\KRISSHORE S\Downloads\email-Eu-core-temporal.txt.gz",
        max_rows=200
    )
    res_email = load_data(req_email)
    
    # 3. Load CDR Data
    req_cdr = IngestionRequest(
        dataset="cdr",
        file_path=r"C:\Users\KRISSHORE S\Downloads\MPD_sample_synthetic_ken_3000subs\MPD_sample_synthetic_ken_3000subs.csv",
        max_rows=100
    )
    res_cdr = load_data(req_cdr)
    
    # 4. Load PaySim Data
    req_paysim = IngestionRequest(
        dataset="paysim",
        file_path=r"C:\PROJECTS\ciran\backend\data\real\archive2\PS_20174392719_1491204439457_log.csv",
        max_rows=100
    )
    res_paysim = load_data(req_paysim)

    # Verification Checks
    print("\n" + "="*50)
    print("PHASE 3 VERIFICATION")
    print("="*50)
    
    # Report Dataset stats
    print("\nDATASET STATS:")
    for res in [res_crime, res_email, res_cdr, res_paysim]:
        print(f"Dataset: {res['dataset']}")
        print(f"  Rows: {res['stats']['records_processed']}")
        print(f"  Entities: {res['stats']['entities_extracted']}")
        print(f"  Relationships: {res['stats']['relationships_created']}")
        print(f"  Alerts: {res['stats']['alerts_generated']}")
    
    # 1. Check patterns (Temporal & Graph Insights)
    print(f"\nPATTERNS: {len(state.patterns)}")
    for p in state.patterns:
        print(f"- {p.category} | {p.title} | {p.confidence}%")
        print(f"  Why: {p.why}")
        print(f"  Evidence: {p.evidence[:3]} {'...' if len(p.evidence) > 3 else ''}")
        
    # 2. Check SAME_AS and POSSIBLE_MATCH edges
    resolution_edges = [r for r in state.relations if r.type in ("SAME_AS", "POSSIBLE_MATCH")]
    print(f"\nENTITY RESOLUTION EDGES: {len(resolution_edges)}")
    for r in resolution_edges:
        print(f"- {r.source} -> {r.target} [{r.type}] (Reason: {r.label})")
        print(f"  Provenance: {r.sourceRecord}")
        
    # 3. Verify cross-case links
    print(f"\nCROSS-CASE LINKS: {len(state.cross_case_links)}")
    for link in state.cross_case_links:
        print(f"- Cases: {link.cases}")
        print(f"- Path: {link.path}")
        print(f"- Summary: {link.summary}")

    # 4. Verify risk alerts
    print(f"\nRISK ALERTS: {len(state.alerts)}")
    if state.alerts:
        # Show detailed factors for first alerted entity
        e_id = state.alerts[0].entities[0]
        ent = next(e for e in state.entities if e.id == e_id)
        print(f"Entity: {ent.id} | {ent.label} | Band: {ent.priorityBand} | Score: {ent.priority}")
        for factor in (ent.priorityFactors or []):
            print(f"  - Factor: {factor.label} (Weight: {factor.weight})")

if __name__ == "__main__":
    verify_phase3()
