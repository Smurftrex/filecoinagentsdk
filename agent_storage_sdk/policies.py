from dataclasses import dataclass
from typing import Optional

@dataclass
class StoragePolicy:
    max_cost_fil: float = 0.0
    redundancy: int = 2
    ttl_days: Optional[int] = 30
    
    def validate(self) -> bool:
        if self.max_cost_fil < 0: return False
        if self.redundancy < 1: return False
        return True
