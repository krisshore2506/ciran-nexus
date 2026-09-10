from typing import Iterator, Dict, Any, List
from abc import ABC, abstractmethod
from models.unified import SourceRecord
from ingestion.validators import ValidationResult

class BaseAdapter(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.validation_result = ValidationResult()

    @abstractmethod
    def stream_records(self, max_rows: int = None) -> Iterator[SourceRecord]:
        """
        Reads the dataset incrementally, applies validation, normalizes rows into the 
        Unified CIRAN Data Model (SourceRecord), and yields them.
        """
        pass
