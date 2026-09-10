from typing import List, Dict, Any
from models.domain import RawRecord

def normalize_records(raw_records: List[RawRecord]) -> List[Dict[str, Any]]:
    """
    Adapter to convert RawRecords into a normalized internal dictionary format 
    that the AI pipelines can process uniformly.
    """
    normalized = []
    for r in raw_records:
        norm = {
            "record_id": r.id,
            "record_type": r.type,
            "timestamp": r.timestamp,
            "source": r.source_system,
            "text_content": "",
            "structured_data": {}
        }
        
        # Flatten content based on type
        if r.type == "case_report":
            norm["text_content"] = r.content.get("text", "")
            norm["structured_data"]["case_id"] = r.content.get("case_id")
            norm["structured_data"]["status"] = r.content.get("status")
        elif r.type == "call_record":
            norm["structured_data"]["caller"] = r.content.get("caller")
            norm["structured_data"]["receiver"] = r.content.get("receiver")
            norm["structured_data"]["name_a"] = r.content.get("subscriber_name_a")
            norm["structured_data"]["name_b"] = r.content.get("subscriber_name_b")
            norm["text_content"] = f"Call between {norm['structured_data']['caller']} and {norm['structured_data']['receiver']}"
        elif r.type == "vehicle_sighting":
            norm["structured_data"]["plate"] = r.content.get("plate_number")
            norm["structured_data"]["location"] = r.content.get("location")
            norm["structured_data"]["driver"] = r.content.get("driver_observed")
        elif r.type == "financial_transaction":
            norm["structured_data"]["sender"] = r.content.get("sender_account")
            norm["structured_data"]["receiver"] = r.content.get("receiver_account")
            norm["structured_data"]["amount"] = r.content.get("amount")
            
        normalized.append(norm)
    return normalized
