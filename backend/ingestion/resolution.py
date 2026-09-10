from typing import Optional

def generate_entity_id(namespace: str, original_id: str) -> str:
    """
    Generates a stable entity ID by strictly namespacing the original ID to prevent 
    fabricated cross-dataset merges. Email '123' becomes 'EMAIL-123' to avoid 
    merging with PaySim '123'.
    """
    if not original_id:
        return f"{namespace}-UNKNOWN"
    return f"{namespace.upper()}-{str(original_id).strip()}"

def generate_relationship_id(source_id: str, target_id: str, rel_type: str, timestamp: Optional[str] = None) -> str:
    """
    Generates a unique relationship ID.
    """
    base = f"{source_id}_{rel_type}_{target_id}"
    if timestamp:
        base += f"_{timestamp}"
    return base
