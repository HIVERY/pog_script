import logging

logger = logging.getLogger(__name__)


class Position():
    def __init__(self, product=None):
        self.product = product  # product
        self.product_upc = product.upc if product is not None else None
        self.performance = None

        # Position location
        self.x = None  # x-coordinate (from left)
        self.y = None  # y-coordinate (from bottom)
        self.z = None  # z-coordinate (from back)

        # Position number of units
        self.base_units_wide = 0  # number of facings not including caps
        self.base_units_high = 0  # number of units not including caps
        self.base_units_deep = 0  # number of units not including caps
        self.base_orientation = None  # int //see orientations below

        # Position x-capping (left/right)
        self.x_cap_units_wide = 0  # number of caps x-direction (left/right)
        self.x_cap_units_high = 0  # x_cap number of units high
        self.x_cap_units_deep = 0  # x_cap number of units deep
        self.x_cap_reversed = False  # False=cap on right, True=cap on left
        self.x_cap_orientation = None  # x_cap base_orientation //see orientations below

        # Position y-capping (top/bottom)
        self.y_cap_units_wide = 0  # number of caps y-direction (top/bottom)
        self.y_cap_units_high = 0  # y_cap number of units high
        self.y_cap_units_deep = 0  # y_cap number of units deep
        self.y_cap_reversed = False  # False=cap above, True=cap below
        self.y_cap_orientation = None  # y_cap base_orientation //see orientations below

        # Position z-capping (front/back)
        self.z_cap_units_wide = 0  # number of caps z-direction (front/back)
        self.z_cap_units_high = 0  # z_cap number of units high
        self.z_cap_units_deep = 0  # z_cap number of units deep
        self.z_cap_reversed = False  # False=cap front??, True=cap back??
        self.z_cap_orientation = None  # z_cap base_orientation //see orientations below

        self.fixture = None  # fixture
        self.number = None  # int //left most position number=1

    # def __str__(self):
    #     # TODO: Return a more useful representation than just the underling UPC
    #     return "UPC: {}".format(self.product.upc)

    @property
    def width(self):
        return self.get_width()

    def get_base_capacity(self):
        """Get the capacity of the position excluding cappings.

        Returns:
            int: Position capacity excluding cappings.
        """
        base_capacity = 1
        if self.product.merch_style == 'TRAY':
            base_capacity = self.product.get_tray_capacity()
        return self.base_units_wide * self.base_units_high * self.base_units_deep * base_capacity

    def get_x_cap_capacity(self):
        """Get the capacity of the x-capping (left/right).

        Returns:
            int: Position x-capping capacity.
        """
        return self.x_cap_units_wide * self.x_cap_units_high * self.x_cap_units_deep

    def get_y_cap_capacity(self):
        """Get the capacity of the y-capping (top/bottom).

        Returns:
            int: Position y-capping capacity.
        """
        return self.y_cap_units_wide * self.y_cap_units_high * self.y_cap_units_deep

    def get_z_cap_capacity(self):
        """Get the capacity of the z-capping (front/back).

        Returns:
            int: Position z-capping capacity.
        """
        return self.z_cap_units_wide * self.z_cap_units_high * self.z_cap_units_deep

    def get_capacity(self):
        """Get the capacity of the position.

        Returns:
            int: Position capacity.
        """
        capacity_excl_caps = self.get_base_capacity()
        x_cap_capacity = self.get_x_cap_capacity()
        y_cap_capacity = self.get_y_cap_capacity()
        z_cap_capacity = self.get_z_cap_capacity()
        return capacity_excl_caps + x_cap_capacity + y_cap_capacity + z_cap_capacity

    def get_base_width(self):
        """Get the width of the position excluding cappings.

        Returns:
            float: Position width excluding cappings.
        """
        if self.base_units_wide == 0:
            return 0.0
        (width, height, depth) = self.product.get_dimensions(self.base_orientation)
        width = width + self.product.finger_space_x
        if self.fixture:
            if self.fixture.divider_between_facings:
                width += self.fixture.divider_width
        return width * self.base_units_wide

    def get_x_cap_width(self):
        """Get the width of the x-capping.

        Returns:
            float: Position x-capping width.
        """
        if self.x_cap_units_wide == 0:
            return 0.0
        (width, height, depth) = self.product.get_dimensions(self.x_cap_orientation)
        if self.fixture:
            if self.fixture.divider_between_facings:
                width += self.fixture.divider_width
        return width * self.x_cap_units_wide

    def get_y_cap_width(self):
        """Get the width of the y-capping.

        Returns:
            float: Position y-capping width.
        """
        if self.y_cap_units_wide == 0:
            return 0.0
        (width, height, depth) = self.product.get_dimensions(self.y_cap_orientation)
        if self.fixture:
            if self.fixture.divider_between_facings:
                width += self.fixture.divider_width
        return width * self.y_cap_units_wide

    def get_z_cap_width(self):
        """Get the width of the z-capping.

        Returns:
            float: Position z-capping width.
        """
        if self.z_cap_units_wide == 0:
            return 0.0
        (width, height, depth) = self.product.get_dimensions(self.z_cap_orientation)
        if self.fixture:
            if self.fixture.divider_between_facings:
                width += self.fixture.divider_width
        return width * self.z_cap_units_wide

    def get_width(self):
        """Get the width of the position.

        Returns:
            float: Position width.
        """
        base_width = self.get_base_width()
        x_cap_width = self.get_x_cap_width()
        return base_width + x_cap_width

    def get_base_height(self):
        """Get the height of the position excluding cappings.

        Returns:
            float: Position height excluding cappings.
        """
        if self.base_units_wide == 0:
            return 0.0
        (width, height, depth) = self.product.get_dimensions(self.base_orientation)
        return height * self.base_units_high

    def get_y_cap_height(self):
        """Get the height of the y-capping.

        Returns:
            float: Position y-capping height.
        """
        if self.y_cap_units_high == 0:
            return 0.0
        (width, height, depth) = self.product.get_dimensions(self.y_cap_orientation)
        return height * self.y_cap_units_high

    def get_height(self):
        """Get the height of the position.

        Returns:
            float: Position height.
        """
        base_height = self.get_base_height()
        y_cap_height = self.get_y_cap_height()
        return base_height + y_cap_height

    def get_base_depth(self):
        """Get the height of the position excluding cappings.

        Returns:
            float: Position height excluding cappings.
        """
        if self.base_units_deep == 0:
            return 0.0
        (width, height, depth) = self.product.get_dimensions(self.base_orientation)
        return depth * self.base_units_deep

    def get_x_cap_depth(self):
        """Get the depth of the x-capping.

        Returns:
            float: Position x-capping depth.
        """
        if self.x_cap_units_deep == 0:
            return 0.0
        (width, height, depth) = self.product.get_dimensions(self.x_cap_orientation)
        return depth * self.x_cap_units_deep

    def get_y_cap_depth(self):
        """Get the depth of the y-capping.

        Returns:
            float: Position y-capping depth.
        """
        if self.y_cap_units_deep == 0:
            return 0.0
        (width, height, depth) = self.product.get_dimensions(self.y_cap_orientation)
        return depth * self.y_cap_units_deep

    def get_z_cap_depth(self):
        """Get the depth of the z-capping.

        Returns:
            float: Position z-capping depth.
        """
        if self.z_cap_units_deep == 0:
            return 0.0
        (width, height, depth) = self.product.get_dimensions(self.z_cap_orientation)
        return depth * self.z_cap_units_deep

    def get_depth(self):
        """Get the depth of the position.

        Returns:
            float: Position depth.
        """
        base_depth = self.get_base_depth()
        z_cap_depth = self.get_z_cap_depth()
        return base_depth + z_cap_depth

    def get_x_midpoint(self):
        """
        Get the midpoint in x axis of this position
        :return: float: midpoint of x axis
        """
        return self.x + (self.get_width() / 2.0)

    def get_linear(self):
        """

        :return: Linear space of position
        """
        return self.get_width()
