import dataclasses

from typing import Any, Tuple, List


@dataclasses.dataclass(frozen=True)
class Descriptions:
    feature: str
    model_name: str 
    descriptions: List[Tuple[str, Any]]
