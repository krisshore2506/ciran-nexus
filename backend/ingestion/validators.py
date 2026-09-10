from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class ValidationResult:
    def __init__(self):
        self.accepted = 0
        self.rejected = 0
        self.warnings = 0
        self.errors: List[str] = []

def validate_row(row: Dict[str, Any], required_fields: List[str]) -> bool:
    """
    Validates a raw dataset row against a list of required fields.
    Returns True if valid, False otherwise.
    """
    for field in required_fields:
        if field not in row or row[field] is None or str(row[field]).strip() == "":
            return False
    return True

def validate_numeric(value: Any) -> bool:
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False
