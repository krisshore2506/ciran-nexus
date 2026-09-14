import httpx
import logging
from typing import List, Optional
from config.settings import settings

class EmbeddingService:
    def __init__(self):
        self.model = "text-embedding-3-small"
        self.dimensions = 1536
        self.api_key = settings.LLM_API_KEY
        
    def embed_texts(self, texts: List[str]) -> Optional[List[List[float]]]:
        """
        Calls OpenAI embeddings API to generate 1536-dimensional vectors for a list of texts.
        Returns None if API key is missing or request fails.
        """
        if not texts:
            return []
            
        if not self.api_key:
            logging.warning("No LLM_API_KEY provided. Cannot generate embeddings.")
            return None
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Note: 'dimensions' parameter is supported for text-embedding-3 models
        payload = {
            "model": self.model,
            "input": texts,
            "dimensions": self.dimensions
        }
        
        try:
            with httpx.Client(timeout=30.0) as client:
                resp = client.post("https://api.openai.com/v1/embeddings", headers=headers, json=payload)
                resp.raise_for_status()
                data = resp.json()
                
                # Extract embeddings matching the input order
                embeddings = [None] * len(texts)
                for item in data.get("data", []):
                    idx = item.get("index")
                    embeddings[idx] = item.get("embedding")
                    
                # Ensure all texts got an embedding
                if any(emb is None for emb in embeddings):
                    logging.error("Some texts did not receive an embedding.")
                    return None
                    
                return embeddings
        except Exception as e:
            logging.error(f"Failed to generate embeddings: {e}")
            return None
