import csv
import logging
import os
import src.templete as temp
from src.templete.utils import get_uom_from_str, parse_float, parse_int, ReadData


logger = logging.getLogger(__name__)


class PSAInterface:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._products = dict()
        self.planogram = None

    @property
    def products(self):
        """
        upc: product object map property.
        """
        return self._products

    def read_psa(self, f, stroe_num=None):
        logger.info('START read_psa %s' % f)
        with ReadData(f, 'cp1252') as fin:
            csv_reader = csv.reader(fin, escapechar='\\')
            next(csv_reader)
            for row in csv_reader:
                # read products
                if str(row[0]) == 'Product':
                    self._read_product_row(row)
                # read planogram
                elif str(row[0]) == 'Planogram':
                    planogram = self._read_planogram_row(row)
                    planogram.store_id = self._get_store_from_filename(f)
                    self.planogram = planogram
                # read segment
                elif str(row[0]) == 'Segment':
                    if planogram is None:
                        raise RuntimeError(
                            'Segment secion is not read before plangorm')
                    segment_number = len(planogram.segments)
                    segment = self._read_segment_row(row, segment_number)
                    segment.planogram_id = planogram.store_id
                    planogram.segments.append(segment)
                # read fixture
                elif str(row[0]) == 'Fixture':
                    if planogram is None:
                        raise RuntimeError(
                            'Fixture row is read before planogram')
                    fixture = self._read_fixture_row(row)
                    if fixture is None:
                        continue
                    for num, segment in enumerate(planogram.segments):
                        # print(num,segment.number)
                        FixtureWidth = fixture.width
                        # print(fixture_width)
                        if fixture.width > 48:
                            # print(fixture_width)
                            FixtureWidth = 48

                        # print('{} >= {} and {} + {} <= {} + {} --{}----{}--'.format(fixture.x,segment.offset_x,fixture.x,fixture.width,segment.offset_x,segment.width,fixture.x >= segment.offset_x ,((fixture.x + fixture.width) <= (segment.offset_x + segment.width))))
                        # print(fixture.type)
                        # print('-----------=======')
                        if fixture.x >= segment.offset_x and (fixture.x + FixtureWidth) <= (segment.offset_x + segment.width):
                            fixture.number = len(segment.shelves)

                            if fixture.type == 0:
                                # It's a shelf
                                fixture.segment_id = segment.number
                                segment.shelves.append(fixture)
                # read position
                elif str(row[0]) == 'Position':
                    if not fixture:
                        logging.error("ERROR: Position is read before fixture")
                        continue
                    position = self._read_position_row(row, fixture, stroe_num)
                    position.fixture = fixture
                    if fixture.type == 0:
                        position.number = len(fixture.positions)
                        # print('postion   ',fixture.name)
                        fixture.positions.append(position)
                        # if position.product_upc == 7199009532:
                        #     print()
                        # print(position.product_upc)
                        # print('--',fixture)

    """ ALL FUNCTIONs """

    def _read_product_row(self, row, overwrite=False):
        upc = parse_int(row[1])
        if upc is None:
            raise RuntimeError('Failed to parse upc from string "{}"'
                               .format(row[1]))
        # if product is None:
        product = temp.Product(upc)
        # add this product in the dict
        self.products[upc] = product
        product.name = str(row[3])
        product.rollup_upc = upc
        product.width = parse_float(row[5], 0.)
        product.height = parse_float(row[6], 0.)
        product.depth = parse_float(row[7], 0.)
        product.size = parse_float(row[10], 0.)
        product.uom = get_uom_from_str(str(row[11]))  # unit of measure
        product.tray_width = parse_float(row[46], 0.)
        product.tray_height = parse_float(row[47], 0.)
        product.tray_depth = parse_float(row[48], 0.)
        product.tray_units_wide = parse_int(row[49], 0)
        product.tray_units_high = parse_int(row[50], 0)
        product.tray_units_deep = parse_int(row[51], 0)
        product.merch_style = 'UNIT'
        if product.tray_units_wide > 0 and product.tray_units_high > 0 and product.tray_units_deep > 0:
            product.merch_style = 'TRAY'
        product.case_size = parse_int(row[60], 0)
        brand_name = str(row[232])
        product.brand = brand_name
        return product

    def _read_planogram_row(self, row):
        name = str(row[1])
        planogram = temp.Planogram(name)
        planogram.height = parse_float(row[4])
        return planogram

    def _read_segment_row(self, row, segment_number):
        segment = temp.Segment(segment_number)
        segment.width = parse_float(row[4])
        segment.height = parse_float(row[6])
        segment.name = str(segment_number)
        segment.offset_x = parse_float(row[10])
        return segment

    def _read_fixture_row(self, row):
        fixture_name = str(row[2])
        fixture_type = parse_int(row[1])
        fixture_assembly = str(row[14])
        fixture_exclude = False
        if fixture_type == 0:  # 0 = shelf
            fixture = temp.Shelf(fixture_name)
            # Shelf merchandisable space
            combine_flag = parse_int(row[37])
            if combine_flag > 0:
                fixture.can_combine = True
                if combine_flag == 1:
                    fixture.combine_direction = "BOTH"
                elif combine_flag == 2:
                    fixture.combine_direction = "LEFT"
                elif combine_flag == 3:
                    fixture.combine_direction = "RIGHT"
                else:
                    logger.error("Unknown combine entry in shelf row {}"
                                 .format(combine_flag))
            elif combine_flag == 0:
                fixture.combine_direction = "NO"
            else:
                fixture.can_combine = False
                fixture.combine_direction = "UNkonw"
                
            fixture.merch_height = parse_float(row[23], 0.0)

            fixture.overhang_back = parse_float(row[31], 0.0)
            # Shelf dividers
            # do not need to consider in this report
            fixture.divider_width = parse_float(row[34])
            fixture.divider_at_start = bool(parse_int(row[151]))
            fixture.divider_at_end = bool(parse_int(row[152]))
            fixture.divider_between_facings = bool(parse_int(row[153]))

        elif fixture_type in [7, 10]:  # 7 = pegboard, 10 = obstruction
            fixture = temp.Fixture(fixture_name)
            # context.add(fixture)
        elif fixture_type == 6:
            # This is a bar and we can skip it.
            return
        else:
            raise RuntimeError(
                'Fixture type {} is unknown'.format(fixture_type))

        fixture.type = fixture_type
        # Fixture overall dimensions
        fixture.width = parse_float(row[5])
        fixture.height = parse_float(row[7])
        fixture.depth = parse_float(row[9])
        # Fixture location
        fixture.x = parse_float(row[4])
        fixture.y = parse_float(row[6])
        fixture.z = parse_float(row[8])
        # Fixture rotation (in degrees)
        fixture.slope = parse_float(row[10])
        # Fixture info
        fixture.assembly = fixture_assembly
        fixture.exclude = fixture_exclude
        if fixture_type == 0:  # 0 = shelf
            fixture.compute_merch_info()
        # print(fixture.divider_width)
        return fixture

    def _read_position_row(self, row, fixture, stroe_num=None):
        number = parse_int(row[44])
        upc = parse_int(row[1])

        product = self.products[upc]
        if product is None:
            self.logger.error(
                'ERROR: Failed to gut product with upc {} for a position'
                .format(upc))
            return

        position = temp.Position(product)

        position.number = number
        position.x = parse_float(row[4], 0.0)
        position.y = parse_float(row[6])
        position.height = parse_float(row[7])
        position.z = parse_float(row[8])
        position.depth = parse_float(row[9])
        position.base_units_wide = parse_int(row[14])
        position.base_units_high = parse_int(row[15])
        position.base_units_deep = parse_int(row[16])
        position.base_orientation = parse_int(row[29])

        position.x_cap_units_wide = parse_int(row[17])
        position.x_cap_reversed = bool(parse_int(row[19]))
        position.x_cap_orientation = parse_int(row[20])
        if position.x_cap_units_wide > 0:
            (width, height, depth) = product.get_dimensions(
                position.x_cap_orientation)
            position.x_cap_units_high = int(fixture.merch_height / height)
            position.x_cap_units_deep = int(fixture.depth / depth)

        if row[21]:
            position.y_cap_units_high = parse_int(row[21])
        if row[23]:
            position.y_cap_reversed = bool(parse_int(row[23]))
        if row[24]:
            position.y_cap_orientation = parse_int(row[24])
        if position.y_cap_units_high > 0:
            (width, height, depth) = product.get_dimensions(
                position.y_cap_orientation)
            position.y_cap_units_wide = int(position.width / width)
            position.y_cap_units_deep = int(fixture.depth / depth)

        if row[25]:
            if int(row[25]):
                with open('zcapping.txt', 'a') as fout:
                    csv_writer = csv.writer(fout, lineterminator='\n')
                    csv_writer.writerow([stroe_num, upc])
            position.z_cap_units_deep = parse_int(row[25])
        if row[27]:
            position.z_cap_reversed = bool(parse_int(row[27]))
        if row[28]:
            position.z_cap_orientation = parse_int(row[28])
        if position.z_cap_units_deep > 0:
            (width, height, depth) = product.get_dimensions(
                position.z_cap_orientation)
            position.z_cap_units_wide = int(position.width / width)
        return position

    def _get_store_from_filename(self, f_name):
        name = os.path.split(f_name)
        store_num = int(name[-1][:4])
        return store_num
