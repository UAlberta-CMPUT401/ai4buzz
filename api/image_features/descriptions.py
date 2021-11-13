import dataclasses

from typing import Any, Tuple, List, Optional


@dataclasses.dataclass(frozen=True)
class Descriptions:
    feature: str
    model_name: str 
    descriptions: List[Tuple[str, Any]]
    processed_image: Optional[bytes] = None
