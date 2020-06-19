
from dataclasses import dataclass, field
from typing import List


@dataclass
class MiniPosition:
    upc: int = None
    number_of_facing_wide: int = None
    number_of_facing_high: int = None
    number_of_facing_deep: int = None


@dataclass
class MiniPlanogram:
    name: str = field(repr=False, default=None)
    coordinate_x: float = field(repr=False, default=None)
    coordinate_y: float = field(repr=False, default=None)
    shelf_width: float = field(repr=False, default=None)
    shelf_height: float = field(repr=False, default=None)
    shelf_depth: float = field(repr=False, default=None)
    merch_width: float = field(repr=False, default=None)
    merch_height: float = field(repr=False, default=None)
    merch_depth: float = field(repr=False, default=None)
    combine_direction: str = field(repr=True, default=None)
    products: List[MiniPosition] = field(repr=False, default_factory=list)
