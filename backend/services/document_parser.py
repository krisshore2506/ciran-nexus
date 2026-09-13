import json
import csv
import io
from typing import Optional

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

class DocumentParser:
    @staticmethod
    def parse_file(filename: str, content: bytes, mime_type: str) -> str:
        """
        Parses a raw file bytes into a single string for NLP extraction.
        Raises ValueError for unsupported formats.
        """
        if not content:
            raise ValueError("File is empty.")

        ext = filename.split('.')[-1].lower() if '.' in filename else ''
        
        if mime_type == "application/pdf" or ext == "pdf":
            return DocumentParser._parse_pdf(content)
            
        elif mime_type == "text/plain" or ext == "txt":
            return content.decode('utf-8', errors='ignore')
            
        elif mime_type == "application/json" or ext == "json":
            return DocumentParser._parse_json(content)
            
        elif mime_type == "text/csv" or ext == "csv":
            return DocumentParser._parse_csv(content)
            
        else:
            raise ValueError(f"Unsupported file type: {mime_type} / {ext}")

    @staticmethod
    def _parse_pdf(content: bytes) -> str:
        if not PyPDF2:
            raise RuntimeError("PyPDF2 is not installed.")
        
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = []
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text.append(extracted)
            return "\n".join(text)
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {e}")

    @staticmethod
    def _parse_json(content: bytes) -> str:
        try:
            data = json.loads(content.decode('utf-8'))
            # Convert JSON structure to a readable string format for NLP
            if isinstance(data, list):
                return "\n".join([json.dumps(d) for d in data])
            return json.dumps(data, indent=2)
        except Exception as e:
            raise ValueError(f"Failed to parse JSON: {e}")

    @staticmethod
    def _parse_csv(content: bytes) -> str:
        try:
            decoded = content.decode('utf-8', errors='ignore')
            reader = csv.reader(io.StringIO(decoded))
            rows = []
            for row in reader:
                rows.append(", ".join(row))
            return "\n".join(rows)
        except Exception as e:
            raise ValueError(f"Failed to parse CSV: {e}")
