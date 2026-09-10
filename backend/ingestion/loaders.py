import json
import csv
from typing import List
from models.domain import RawRecord

def load_json(filepath: str) -> List[RawRecord]:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [RawRecord(**item) for item in data]

def load_csv(filepath: str) -> List[RawRecord]:
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Assuming CSV maps row fields to content
            record = RawRecord(
                id=row.get('id', ''),
                type=row.get('type', 'unknown'),
                timestamp=row.get('timestamp', ''),
                source_system=row.get('source_system', 'csv'),
                content=row
            )
            records.append(record)
    return records
