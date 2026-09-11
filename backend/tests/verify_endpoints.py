import httpx
import json
import traceback

BASE_URL = "http://localhost:8000"

def verify():
    results = {}
    try:
        # 4. Run POST /api/ingestion/load
        print("--- POST /api/ingestion/load ---")
        res = httpx.post(f"{BASE_URL}/api/ingestion/load")
        res.raise_for_status()
        ingestion_data = res.json()
        print(json.dumps(ingestion_data, indent=2))
        results['ingestion'] = ingestion_data
        
        # 5. Verify entities are created
        print("\n--- GET /api/entities ---")
        res = httpx.get(f"{BASE_URL}/api/entities")
        res.raise_for_status()
        entities = res.json()
        print(f"Total entities: {len(entities)}")
        print("First entity:")
        if entities:
            print(json.dumps(entities[0], indent=2))
        results['entities'] = entities
        
        # 6. Verify relationships & neighbour traversal (network)
        print("\n--- GET /api/network ---")
        res = httpx.get(f"{BASE_URL}/api/network")
        res.raise_for_status()
        network = res.json()
        print(f"Nodes: {len(network['nodes'])}, Edges: {len(network['edges'])}")
        print("First edge:")
        if network['edges']:
            print(json.dumps(network['edges'][0], indent=2))
        results['network'] = network
            
        # 6b. Verify individual entity network
        if entities:
            ent_id = entities[0]['id']
            print(f"\n--- GET /api/entities/{ent_id}/network ---")
            res = httpx.get(f"{BASE_URL}/api/entities/{ent_id}/network")
            res.raise_for_status()
            ent_network = res.json()
            print(f"Entity {ent_id} Network Nodes: {len(ent_network['nodes'])}, Edges: {len(ent_network['edges'])}")
            
        # 7. Verify cross-case correlation
        print("\n--- GET /api/cross-case ---")
        res = httpx.get(f"{BASE_URL}/api/cross-case")
        res.raise_for_status()
        cross_cases = res.json()
        print(f"Total cross-case links: {len(cross_cases)}")
        if cross_cases:
            print(json.dumps(cross_cases[0], indent=2))
        results['cross_case'] = cross_cases
            
        # 8. Verify risk scores / alerts
        print("\n--- GET /api/alerts ---")
        res = httpx.get(f"{BASE_URL}/api/alerts")
        res.raise_for_status()
        alerts = res.json()
        print(f"Total alerts: {len(alerts)}")
        if alerts:
            print(json.dumps(alerts[0], indent=2))
        results['alerts'] = alerts
            
        # 9. Verify evidence provenance
        print("\n--- GET /api/evidence/{id} ---")
        if cross_cases and len(cross_cases[0].get('evidence', [])) > 0:
            ev_id = cross_cases[0]['evidence'][0]
            res = httpx.get(f"{BASE_URL}/api/evidence/{ev_id}")
            res.raise_for_status()
            evidence = res.json()
            print(json.dumps(evidence, indent=2))
            results['evidence'] = evidence
        else:
            print("No evidence IDs found in cross_case to look up.")
            
        # 10. Verify POST /api/copilot/query
        print("\n--- POST /api/copilot/query ---")
        res = httpx.post(f"{BASE_URL}/api/copilot/query", json={"query": "Ravi and 203"})
        res.raise_for_status()
        copilot = res.json()
        print(json.dumps(copilot, indent=2))
        results['copilot'] = copilot
        
        # 11. Verify POST /api/reports/generate
        print("\n--- POST /api/reports/generate ---")
        res = httpx.post(f"{BASE_URL}/api/reports/generate")
        res.raise_for_status()
        report = res.json()
        print(json.dumps(report, indent=2))
        results['report'] = report
        
        # 12. Verify GET /api/kpis
        print("\n--- GET /api/kpis ---")
        res = httpx.get(f"{BASE_URL}/api/kpis")
        res.raise_for_status()
        kpis = res.json()
        print(f"Total KPIs: {len(kpis)}")
        if kpis:
            print(json.dumps(kpis[0], indent=2))
        results['kpis'] = kpis
        
        # 13. Verify GET /api/timeline
        print("\n--- GET /api/timeline ---")
        res = httpx.get(f"{BASE_URL}/api/timeline")
        res.raise_for_status()
        timeline = res.json()
        print(f"Total timeline events: {len(timeline)}")
        if timeline:
            print(json.dumps(timeline[0], indent=2))
        results['timeline'] = timeline
        
        print("\nVERIFICATION COMPLETE")
    except Exception as e:
        print(f"\nERROR DURING VERIFICATION: {e}")
        traceback.print_exc()
        
if __name__ == "__main__":
    verify()
