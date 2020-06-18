
import logging

logger = logging.getLogger(__name__)


class Product():
    def __init__(self, upc):
        self.upc = upc                  # product upc
        self.rollup_upc = None          # product rollup upc
        self.description = None         # product description
        self.rollup_description = None  # product rollup description
        self.category = None            # product category
        self.subcategory = None         # product subcategory
        self.subsubcategory = None      # product subsubcategory
        self.brand = None               # product brand
        self.subbrand = None            # product subbrand
        self.package_group = None       # product package group
        self.package_type = None        # product package type
        self.manufacturer = None        # product manufacturer
        self.size = None                # product size
        self.uom = None                 # product unit of measure
        self.case_pack = None           # product case pack
        self.height = None              # product height
        self.width = None               # product width
        self.depth = None               # product depth
        self.price_tier = None          # product price tier
        self.tray_width = 0             # product tray width
        self.tray_height = 0            # product tray height
        self.tray_depth = 0             # product tray depth
        self.tray_units_wide = 0        # product tray number of units wide
        self.tray_units_high = 0        # product tray number of units high
        self.tray_units_deep = 0        # product tray number of units deep
        self.finger_space_x = 0         # product finger space x

    def print_product(self):
        print('PRODUCT:', self.upc, self.description)

    def get_size(self, unit_of_measure):
        oz_in_ml = 0.03381402
        if unit_of_measure == UnitOfMeasure.oz:
            if self.uom == UnitOfMeasure.oz:
                return self.size
            elif self.uom in [UnitOfMeasure.l, UnitOfMeasure.ml]:
                # Convert to ml
                if self.uom == UnitOfMeasure.l:
                    size = self.size * 1000
                elif self.uom == UnitOfMeasure.ml:
                    size = self.size
                # Convert to oz
                return size * oz_in_ml
            elif self.uom == UnitOfMeasure.unknown:
                return self.size
            else:
                logger.error("Unknown UoM {}".format(self.uom))
                return self.size
        elif unit_of_measure in [UnitOfMeasure.l, UnitOfMeasure.ml]:
            if self.uom == UnitOfMeasure.l:
                if unit_of_measure == UnitOfMeasure.l:
                    return self.size
                elif unit_of_measure == UnitOfMeasure.ml:
                    return self.size * 10000
            elif self.uom == UnitOfMeasure.ml:
                if unit_of_measure == UnitOfMeasure.l:
                    return self.size / 1000
                elif unit_of_measure == UnitOfMeasure.ml:
                    return self.size
            elif self.uom == UnitOfMeasure.oz:
                # Convert to ml
                size = self.size / oz_in_ml
                # Return the one we want
                if unit_of_measure == UnitOfMeasure.l:
                    return size / 1000
                elif unit_of_measure == UnitOfMeasure.ml:
                    return size
            elif self.uom == UnitOfMeasure.unknown:
                return self.size
            else:
                logger.error("Unknown UoM {} for product {}".format(
                    self.uom, self.upc))
                return self.size

    def get_tray_capacity(self):
        return self.tray_units_wide * self.tray_units_high * self.tray_units_deep

    def get_dimensions(self, orientation_face, rotation=None):
        """
        Python doesn't have multiple dispatch, so detect how we are using this by number of arguments
        :param orientation_face: orientation int or displayed face
        :param rotation: optional rotation of face
        :return:
            (float, float, float): tuple of product dimensions (width, height,
            depth)
        """
        if rotation is not None:
            return self.get_dimensions_face_rotation(orientation_face, rotation)
        else:
            # We just have orientation int
            return self.get_dimensions_orientation_int(orientation_face)

    def get_dimensions_orientation_int(self, orientation, merch_style="UNIT"):
        """Get the dimensions of the product.

        Returns:
            (float, float, float): tuple of product dimensions (width, height,
            depth)
        """
        if merch_style == 'UNIT':
            width = self.width
            height = self.height
            depth = self.depth
        elif merch_style == 'TRAY':
            width = self.tray_width
            height = self.tray_height
            depth = self.tray_depth
        # 0=front, 6=back, 12=front180, 18=back180
        if orientation in set([0, 6, 12, 18]):
            merch_width = width
            merch_height = height
            merch_depth = depth
        # 1=front90, 7=back90, 13=front270, 19=back270
        elif orientation in set([1, 7, 13, 19]):
            merch_width = height
            merch_height = width
            merch_depth = depth
        # 2=side, 8=right, 14=side180, 20=right180
        elif orientation in set([2, 8, 14, 20]):
            merch_width = depth
            merch_height = height
            merch_depth = width
        # 3=side90, 9=right90, 15=side270, 21=right270
        elif orientation in set([3, 9, 15, 21]):
            merch_width = height
            merch_height = depth
            merch_depth = width
        # 4=top, 10=base, 16=top180, 22=base180
        elif orientation in set([4, 10, 16, 22]):
            merch_width = width
            merch_height = depth
            merch_depth = height
        # 5=top90, 11=base90, 17=top270, 23=base270
        elif orientation in set([5, 11, 17, 23]):
            merch_width = depth
            merch_height = width
            merch_depth = height
        else:
            logger.error('ERROR: unknown orientation {} for product {}'.format(
                orientation, self.upc))
            return 0.0, 0.0, 0.0
        return merch_width, merch_height, merch_depth

    def get_dimensions_face_rotation(self, face, rotation):
        """Get the dimensions of the product. With face/rotation definition of dimensions

        Returns:
            (float, float, float): tuple of product dimensions (width, height,
            depth)
        """
        width = height = depth = None
        if face == 1:
            depth = self.depth
            if rotation == 0:
                width = self.width
                height = self.height
            elif rotation == 1:
                width = self.height
                height = self.width
        elif face == 2:
            depth = self.height
            if rotation == 0:
                width = self.width
                height = self.depth
            elif rotation == 1:
                width = self.depth
                height = self.width
        elif face == 3:
            depth = self.width
            if rotation == 0:
                width = self.depth
                height = self.height
            elif rotation == 1:
                width = self.height
                height = self.depth

        if (not width) or (not height) or (not depth):
            logger.error('ERROR: unknown orientation ({}, {}) for product {}'.format(
                face, rotation, self.upc))
            return 0.0, 0.0, 0.0
        else:
            return width, height, depth

    def get_square(self, orientation):
        """Get the square space (area) of the product.

        Returns:
            float: square space (area) of the product.
        """

        (width, height, depth) = self.get_dimensions(orientation)
        return width * depth

    def get_cubic(self):
        """Get the cubic space (volume) of the product.

        Returns:
            float: cubic space (volume) of the product.
        """
        return self.width * self.height * self.depth

