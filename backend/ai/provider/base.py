from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_answer(self, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        """
        Generate a structured answer from the LLM.
        Expected return format:
        {
            "answer": str,
            "facts": List[str],
            "derived_findings": List[str],
            "limitations": List[str],
            "evidence_ids": List[str]
        }
        Return None if the provider fails, times out, or returns invalid structure.
        """
        pass
