import dataclasses

from typing import Dict, Any, Tuple


@dataclasses.dataclass(frozen=True)
class Descriptions:
    feature: str
    model_name: str 
    descriptions: Tuple[str, float]
