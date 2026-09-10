import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.routes.ingestion import load_data, IngestionRequest
from api.routes.copilot import ask_copilot, CopilotRequest
from api.state import state

def verify_phase4():
    # 1. Load Crime Data
    req_crime = IngestionRequest(
        dataset="crime",
        file_path=r"C:\PROJECTS\ciran\backend\data\real\archive1\crime_dataset_india.csv",
        max_rows=100
    )
    load_data(req_crime)

    # 2. Load Email Data
    req_email = IngestionRequest(
        dataset="email",
        file_path=r"C:\Users\KRISSHORE S\Downloads\email-Eu-core-temporal.txt.gz",
        max_rows=200
    )
    load_data(req_email)
    
    # 3. Load CDR Data
    req_cdr = IngestionRequest(
        dataset="cdr",
        file_path=r"C:\Users\KRISSHORE S\Downloads\MPD_sample_synthetic_ken_3000subs\MPD_sample_synthetic_ken_3000subs.csv",
        max_rows=100
    )
    load_data(req_cdr)
    
    # 4. Load PaySim Data
    req_paysim = IngestionRequest(
        dataset="paysim",
        file_path=r"C:\PROJECTS\ciran\backend\data\real\archive2\PS_20174392719_1491204439457_log.csv",
        max_rows=100
    )
    load_data(req_paysim)
    
    # Extract known entities to query
    paysim_entities = [e for e in state.entities if "PAYSIM" in e.id]
    crime_cases = [e for e in state.entities if e.type.lower() == "case"]
    
    if not crime_cases:
        print("DEBUG: No cases found. Available entities:", [e.id for e in state.entities[:5]])
        return

    print("\n" + "="*50)
    print("PHASE 4 REAL DATA COPILOT VERIFICATION")
    print("="*50)
    
    queries = [
        ("Entity Context Query", f"Show connections for {paysim_entities[0].id}"),
        ("Risk Explanation Query", f"Why is {paysim_entities[0].id} flagged?"),
        ("Cross-Case Query", f"What connects {crime_cases[0].id}?"),
        ("Timeline Query", f"Give me the timeline for {paysim_entities[0].id}"),
        ("Case Summary", f"Summarize case {crime_cases[0].id}"),
        ("Insufficient Evidence", "Tell me about John Doe the non-existent person")
    ]
    
    for title, q in queries:
        print(f"\n--- {title} ---")
        print(f"User: {q}")
        res = ask_copilot(CopilotRequest(query=q))
        print(f"Copilot:")
        print(res.summary)
        print(f"\nEvidence: {res.evidence}")
        print(f"Chips: {res.chips}")
        print(f"Caution: {res.caution}")

if __name__ == "__main__":
    verify_phase4()
