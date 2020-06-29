from src.templete.psa import PSAInterface
from src.templete.planogram import Planogram
from src.templete.utils import dynamicCombine, validate_combined_shelves
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
        dup = psa.read_psa(path)
        if not isinstance(dup, Planogram):
            return
        planogram = psa.planogram
        planogram.calculate_merch_dimensions()
        key_set = sorted(
            set([shelf.coordinate_y for shelf in planogram.mini_planogram_set]))
        lis = []
        for coordinate_y in key_set:
            combine = []
            for shelf in sorted(planogram.mini_planogram_set, key=lambda x: x.coordinate_x):
                if shelf.coordinate_y == coordinate_y:
                    combine.append(shelf)
            lis.append(combine)
        shelf_combine = [dynamicCombine(shl) for shl in lis]
        new_shelf_combine, fail = validate_combined_shelves(shelf_combine)
        # check all combined shevles if can not combine, split
        while fail:
            new_shelf_combine, fail = validate_combined_shelves(new_shelf_combine)
        fname = os.path.join(out, os.path.basename(
            path).replace('.psa', '.csv'))
        with open(fname, 'w') as fout:
            writer = csv.writer(fout)
            header = ["shelf_name", "coordinate_x", "coordinate_y", "shelf_width",
                      "shelf_height", "shelf_depth", "merch_width", "merch_height", 'merch_depth']
            writer.writerow(header)
            for shelf in shelf_combine:
                for cb in shelf:
                    shelf_width, merch_width, products = 0, 0, []
                    for sf in cb:
                        shelf_width += sf.shelf_width
                        merch_width += sf.merch_width
                        products += sf.products
                    row = [" * ".join([shel.name for shel in cb]),
                           cb[0].coordinate_x,
                           cb[0].coordinate_y,
                           shelf_width,
                           cb[0].shelf_height,
                           cb[0].shelf_depth,
                           merch_width,
                           cb[0].merch_height,
                           cb[0].merch_depth]
                    writer.writerow(row)
                    for mini_p in products:
                        writer.writerow([mini_p.upc, mini_p.number_of_facing_wide, mini_p.number_of_facing_high,
                                        mini_p.number_of_facing_deep])

    if os.path.isfile(path):
        process(path, out)
    elif os.path.isdir(path):
        if not out:
            print("\033[91m")
            print('ERROR: Output folder was not specified, using `-o` flag to specify output folder for batch run.')
            print("\033[0m")
            return
        if not os.path.exists(out):
            os.mkdir(os.path.join(os.getcwd(), out))
        for dirpath, subdirs, files in os.walk(path):
            for x in tqdm.tqdm(files):
                if x.endswith(".psa"):
                    process(os.path.join(dirpath, x), out)
    else:
        print("\033[91m")
        print("ERROR: Can not find psa files")
        print("\033[0m")
