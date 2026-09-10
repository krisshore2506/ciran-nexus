import httpx
import json

BASE_URL = "http://localhost:8000"

def dump():
    endpoints = [
        ("POST", "/api/ingestion/load", None),
        ("GET", "/api/entities", None),
        ("GET", "/api/network", None),
        ("GET", "/api/entities/P-RAVI/network", None),
        ("GET", "/api/cross-case", None),
        ("GET", "/api/alerts", None),
        ("GET", "/api/evidence/EV-3", None), # From previous run we know EV-3 is a cross-case evidence
        ("POST", "/api/copilot/query", {"query": "Ravi and 203"}),
        ("POST", "/api/reports/generate", None)
    ]
    
    with open("tests/evidence_dump.txt", "w") as f:
        for method, path, data in endpoints:
            f.write(f"\n=======================================================\n")
            f.write(f"REQUEST: {method} {path}\n")
            if data:
                f.write(f"BODY: {json.dumps(data)}\n")
            try:
                if method == "GET":
                    res = httpx.get(f"{BASE_URL}{path}")
                else:
                    res = httpx.post(f"{BASE_URL}{path}", json=data)
                f.write(f"STATUS CODE: {res.status_code}\n")
                f.write(f"RESPONSE:\n{json.dumps(res.json(), indent=2)}\n")
            except Exception as e:
                f.write(f"ERROR: {str(e)}\n")

if __name__ == "__main__":
    dump()
