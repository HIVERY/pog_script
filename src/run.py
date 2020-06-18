from src.templete.psa import PSAInterface
import click
from collections import defaultdict
import os
import csv
import tqdm


@click.command()
@click.option(
    "--path",
    "-p",
    help="The path to psa file.",
    required=True
)
@click.option(
    "--out",
    "-o",
    default='',
    help="The path to output file.",
)
def extract(path, out):

    def process(path, out):
        psa = PSAInterface()
        psa.read_psa(path)
        planogram = psa.planogram
        planogram.calculate_merch_dimensions()
        key_set = sorted(
            set([shelf.coordinate_y for shelf in planogram.mini_planogram_set]))
        p_dict = defaultdict(list)
        for coordinate_y in key_set:
            combine = []
            for shelf in sorted(planogram.mini_planogram_set, key=lambda x: x.coordinate_x):
                if shelf.coordinate_y == coordinate_y:
                    if shelf.combine_direction in ["RIGHT", "BOTH"]:
                        combine.append(shelf)
                    if shelf.combine_direction == "LEFT":
                        combine.append(shelf)
                        # print(shelf.name)
                        number = ','.join(
                            [shelf.name.split('-', 1)[1].strip() if '-' in shelf.name else shelf.name.split(' ')[-1].strip() for shel in combine])
                        key = "".join([shelf.name.split('-', 1)
                                       [0], "- ", "[", number, "]"])
                        p_dict[key] = combine
                        combine = []
        fname = os.path.join(out, os.path.basename(
            path).replace('.psa', '.csv'))
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

    if os.path.isfile(path):
        process(path, out)
    elif os.path.isdir(path):
        for dirpath, subdirs, files in os.walk(path):
            for x in tqdm.tqdm(files):
                if x.endswith(".psa"):
                    process(os.path.join(dirpath, x), out)
    else:
        print("\033[91m")
        print("ERROR: Can not find psa files")
        print("\033[0m")
