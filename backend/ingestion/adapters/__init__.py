from .base_adapter import BaseAdapter
from .crime_adapter import CrimeAdapter
from .email_adapter import EmailAdapter
from .cdr_adapter import CDRAdapter
from .paysim_adapter import PaySimAdapter

ADAPTER_REGISTRY = {
    "crime": CrimeAdapter,
    "email": EmailAdapter,
    "cdr": CDRAdapter,
    "paysim": PaySimAdapter
}

def get_adapter(dataset_name: str, file_path: str) -> BaseAdapter:
    if dataset_name not in ADAPTER_REGISTRY:
        raise ValueError(f"Unknown dataset adapter: {dataset_name}")
    return ADAPTER_REGISTRY[dataset_name](file_path)
