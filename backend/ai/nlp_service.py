import re
from typing import List, Dict, Any

def extract_entities_from_text(text: str) -> List[Dict[str, Any]]:
    """
    Mock NLP service. Uses regex/rules to simulate NER on unstructured text.
    In a real implementation, this would call spaCy, HuggingFace, or an LLM.
    """
    entities = []
    
    # Very basic regex rules to simulate NER for the synthetic dataset
    persons = re.findall(r'(Ravi Kumar|Arjun Kumar|Karthik Raj|Mohan Das|Priya Shah)', text)
    for p in set(persons):
        entities.append({"type": "person", "value": p, "confidence": 85})
        
    locations = re.findall(r'(Location [A-Z])', text)
    for l in set(locations):
        entities.append({"type": "location", "value": l, "confidence": 90})
        
    vehicles = re.findall(r'(TN-[A-Z]{2}-\d{4})', text)
    for v in set(vehicles):
        entities.append({"type": "vehicle", "value": v, "confidence": 95})
        
    phones = re.findall(r'(XXXXX\d{4})', text)
    for ph in set(phones):
        entities.append({"type": "phone", "value": ph, "confidence": 95})
        
    accounts = re.findall(r'(AC-XXXX-\d{3})', text)
    for ac in set(accounts):
        entities.append({"type": "account", "value": ac, "confidence": 95})
        
    cases = re.findall(r'(CASE-\d{3})', text)
    for c in set(cases):
        entities.append({"type": "case", "value": c, "confidence": 99})

    return entities
