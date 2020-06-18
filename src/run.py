from src.templete.psa import PSAInterface
import click
from collections import defaultdict
import pprint
import os
import csv


@click.command()
@click.option(
    "--path",
    "-p",
    help="The path to psa file.",
    required=True
)
def extract(path):
    psa = PSAInterface()
    psa.read_psa(path)
    planogram = psa.planogram
    planogram.calculate_merch_dimensions()
    key_set = sorted(
        set([shelf.coordinate_y for shelf in planogram.mini_planogram_set]))
    print(key_set)
    p_dict = defaultdict(list)
    for coordinate_y in key_set:
        combine = []
        for shelf in sorted(planogram.mini_planogram_set, key=lambda x: x.coordinate_x):
            if shelf.coordinate_y == coordinate_y:
                # input(shelf)
                if shelf.combine_direction in ["RIGHT", "BOTH"]:
                    combine.append(shelf)
                if shelf.combine_direction == "LEFT":
                    combine.append(shelf)
                    number = ','.join(
                        [shel.name.split('-')[1].strip() for shel in combine])
                    key = shelf.name.split('-')[0] + "[" + number + "]"
                    p_dict[key] = combine
                    combine = []
    pprint.pprint(p_dict)
    input()
    fname = os.path.basename(path).replace('.psa', '.csv')
    print(fname)
    with open(fname, 'w') as fout:
        writer = csv.writer(fout)
        header = ["Shelf_name", "coordinate_x", "coordinate_y", "shelf_width",
                  "shelf_height", "shelf_depth", "merch_width", "merch_height", 'merch_depth']
        writer.writerow(header)
        for k, v in p_dict.items():

            shelf_width, merch_width, products = 0, 0, []
            for shelf in v:
                shelf_width += shelf.shelf_width
                merch_width += shelf.merch_width
                products += shelf.products
            row = [k,
                   v[0].coordinate_x,
                   v[0].coordinate_y,
                   shelf_width,
                   v[0].shelf_height,
                   v[0].shelf_depth,
                   merch_width,
                   v[0].merch_height,
                   v[0].merch_depth,
                   ]
            writer.writerow(row)
            for upc in products:
                writer.writerow([upc])
