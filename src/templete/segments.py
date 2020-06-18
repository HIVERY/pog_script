import logging


logger = logging.getLogger(__name__)


class Segment():
    def __init__(self, number):
        self.number = number
        self.planogram_id = None

        self.width = None
        self.height = None
        self.depth = None

        self.offset_x = 0.0
        # fixture trated as shelf here
        # self.fixtures = list()
        self.shelves = list()

    def sort_lists(self):
        # self.fixtures.sort(key=lambda fixture: fixture.y,reverse=True)
        self.shelves.sort(key=lambda fixture: fixture.y, reverse=True)
        # print(self.shelves)


class Fixture():
    def __init__(self, name):
        self.name = name
        self.number = None
        self.width = None
        self.type = None  # 0=shelf, 7=pegboard, 10=obstruction

        # Fixture overall dimensions
        self.width = None
        self.heigt = None
        self.depth = None

        # Fixture location
        self.x = None  # x-coordinate (from left)
        self.y = None  # y-coordinate (from bottom)
        self.z = None  # z-coordinate (from back)

        self.dip = 0
        self.slope = 0
        self.angle = 0
        self.angle = 0
        self.roll = 0

        self.assmbly = None
        self.exclude = False

        self.positions = list()


class Shelf(Fixture):
    def __init__(self, name):
        super().__init__(name)
        self.level = None
        self.can_combine = False
        self.combine_direction = "BOTH"
        self.merch_height = 0.0  # merchandisable height
        self.merch_depth = 0.0  # merchandisable depth
        self.merch_start_x = 0.0  # the real start of available space
        self.merch_end_x = 0.0  # the real end of available space
        self.overhang_back = 0.0
        self.excluded_width = 0.0

    @property
    def merch_width(self):
        return self.get_merch_width()

    def get_merch_width(self):
        merch_width = self.merch_end_x - self.merch_start_x
        return merch_width

    def get_liner(self):
        liner = 0.0
        for position in self.positions:
            liner += position.get_linear()
        return liner

    def compute_merch_info(self):
        """ compute the actual width and x coords """
        """ not consider the divider width in this case """
        self.merch_start_x = self.x
        self.merch_end_x = self.x + self.width
