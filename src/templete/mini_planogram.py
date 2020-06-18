
from dataclasses import dataclass, field
from typing import List


@dataclass
class MiniPlanogram:
    name: str = None
    coordinate_x: float = None
    coordinate_y: float = None
    shelf_width: float = None
    shelf_height: float = None
    shelf_depth: float = None
    merch_width: float = None
    merch_height: float = None
    merch_depth: float = None
    combine_direction: str = None
    products: List[int] = field(default_factory=list)
