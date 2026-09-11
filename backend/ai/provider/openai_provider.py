import httpx
import json
import logging
from typing import Dict, Any, Optional
from config.settings import settings
from .base import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = settings.LLM_API_KEY
        self.endpoint = "https://api.openai.com/v1/chat/completions"
        self.model = "gpt-4o-mini"
        
    def generate_answer(self, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        if not self.api_key:
            logging.warning("OpenAIProvider: API key missing, falling back to deterministic.")
            return None
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.0,
            "response_format": {"type": "json_object"}
        }
        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(self.endpoint, headers=headers, json=payload)
                response.raise_for_status()
                
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                parsed = json.loads(content)
                
                required_keys = {"answer", "facts", "derived_findings", "limitations", "evidence_ids"}
                if not required_keys.issubset(parsed.keys()):
                    logging.error("OpenAIProvider returned incomplete structure.")
                    return None
                    
                return parsed
                
        except (httpx.RequestError, httpx.HTTPStatusError, json.JSONDecodeError, KeyError, IndexError) as e:
            logging.error(f"OpenAIProvider generation failed safely: {str(e)}")
            return None
