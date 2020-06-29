import logging
import math
from .mini_planogram import MiniPlanogram, MiniPosition
from .utils import pairwise

logger = logging.getLogger(__name__)


class Planogram:
    def __init__(self, name):
        self.name = name
        self.height = .0
        self.has_obstructions = False
        self.parent_id = None
        self.combined_shelves = list()
        self.sales_per_week = 0.
        self.units_per_week = 0.
        self.dos = float('inf')
        self.segments = list()
        self.store_id = None
        self.mini_planogram_set = list()

    @property
    def shelves(self):
        for s in self.segments:
            yield from s.shelves

    @property
    def positions(self):
        for f in self.shelves:
            yield from f.positions

    def get_capacity(self, upc):
        capacity = 0
        for position in self.positions:
            if position.product.upc == upc:
                capacity += position.get_capacity()
        return capacity

    def get_linear(self, upc):
        linear = 0.0
        for position in self.positions:
            if position.product.upc == upc:
                linear += position.get_width()
        return linear

    def get_min_x(self, upc):
        min_x = ''
        for position in self.positions:
            if position.product.upc == upc:
                if min_x == '':
                    min_x = position.x
                else:
                    if position.x < min_x:
                        min_x = position.x
        return min_x

    def get_max_x(self, upc):
        max_x = ''
        for position in self.positions:
            if position.product.upc == upc:

                if max_x == '':
                    max_x = position.x
                else:
                    if position.x > max_x:
                        max_x = position.x
        return max_x

    def get_min_y(self, upc):
        min_y = ''
        for position in self.positions:
            if position.product.upc == upc:
                if min_y == '':
                    min_y = position.y
                else:
                    if position.y < min_y:
                        min_y = position.y
        return min_y

    def get_max_y(self, upc):
        max_y = ''
        for position in self.positions:
            if position.product.upc == upc:
                if max_y == '':
                    max_y = position.y
                else:
                    if position.y > max_y:
                        max_y = position.y
        return max_y

    def get_number_of_facing(self, upc):
        number_of_facing = 0.0
        for position in self.positions:
            if position.product.upc == upc:
                number_of_facing = position.base_units_wide
                return number_of_facing
        return number_of_facing

    def sort_lists(self):
        for segment in self.segments:
            segment.sort_lists()

    def calculate_missing_merch_heights(self, keep_existing=False):
        for segment in self.segments:
            for shelf1, shelf2 in pairwise(segment.shelves):
                if shelf2.merch_height > 0 and keep_existing:
                    # If we have a merch height, continue to next pair
                    continue
                if shelf1.slope < 0:
                    shelf1_min_y = shelf1.y + shelf1.depth * \
                        math.sin(math.radians(shelf1.slope))
                else:
                    shelf1_min_y = shelf1.y
                shelf2.merch_height = shelf1_min_y - shelf2.height - shelf2.y
            try:
                shelf = segment.shelves[0]

                if shelf.slope < 0:
                    shelf_min_y = shelf.y + shelf.depth * \
                        math.sin(math.radians(shelf.slope))
                else:
                    shelf_min_y = shelf.y
                if shelf.merch_height > 0 and keep_existing:
                    # If the last shelf has a merch height, continue to next segment
                    continue
                fixture_above = False
                fixture_above_y = 0
                for fixture in segment.shelves:
                    if fixture.y > shelf.y:
                        fixture_above_y = max(fixture_above_y, fixture.y)
                        fixture_above = True
                if fixture_above:
                    shelf.merch_height = fixture_above_y - shelf_min_y - shelf.height
                elif segment.height:
                    if segment.height > 0:
                        shelf.merch_height = segment.height - shelf_min_y - shelf.height
                elif self.height:
                    if self.height > 0:
                        shelf.merch_height = self.height - shelf_min_y - shelf.height
                else:
                    logger.error(
                        "ERROR: No known height above (segment/planogram) for shelf {}".format(shelf.name))
                    shelf.merch_height = 20
            except IndexError:
                logging.error('index error')

    def calculate_levels(self):
        for segment in self.segments:
            curr_level = 1
            segment.shelves.sort(key=lambda x: x.y)  # ISO
            for shelf in segment.shelves:
                if not shelf.exclude:
                    shelf.level = curr_level
                    curr_level += 1

    def calculate_merch_depths(self):
        for segment in self.segments:
            pegboard_depth = 0.0
            for fixture in segment.shelves:
                if fixture.type == 7:
                    # This is a pegboard
                    pegboard_depth = fixture.depth
                    break
            for shelf in segment.shelves:
                depth_to_pegboard = shelf.depth + shelf.z - pegboard_depth
                depth_with_overhang = shelf.depth + shelf.overhang_back
                shelf.merch_depth = min(depth_to_pegboard, depth_with_overhang)

    def caculate_z_capping(self):
        for seg in self.segments:
            for shel in seg.shelves:
                for pos in shel.positions:
                    if pos.z_cap_units_deep > 0:
                        (width, height, depth) = pos.product.get_dimensions(
                            pos.z_cap_orientation)
                        pos.z_cap_units_high = int(shel.merch_height / height)

    def extract_mini_info(self):
        for seg in self.segments:
            for shel in seg.shelves:
                mini = MiniPlanogram()
                mini.name = shel.name
                mini.coordinate_x = shel.x
                mini.coordinate_y = shel.y
                mini.shelf_angle = shel.angle
                mini.shelf_slope = shel.slope
                mini.shelf_width = shel.width
                mini.shelf_height = shel.height
                mini.shelf_depth = shel.depth
                mini.merch_width = shel.get_merch_width()
                mini.merch_height = shel.merch_height
                mini.merch_depth = shel.merch_depth
                mini.combine_direction = shel.combine_direction
                for pos in shel.positions:
                    mini_p = MiniPosition(
                        upc=pos.product_upc,
                        number_of_facing_wide=pos.base_units_wide,
                        number_of_facing_high=pos.base_units_high,
                        number_of_facing_deep=pos.base_units_deep,
                    )
                    mini.products.append(mini_p)
                if mini not in self.mini_planogram_set:
                    self.mini_planogram_set.append(mini)

    def calculate_merch_dimensions(self, calculate_segment_dimensions=True):
        self.sort_lists()
        self.calculate_merch_depths()
        self.calculate_missing_merch_heights()
        # self.exclude_shelves_due_to_merch_space()
        # self.caculate_z_capping()
        self.calculate_levels()
        self.extract_mini_info()
        # if calculate_segment_dimensions:
        #     self.calculate_segment_dimensions()
