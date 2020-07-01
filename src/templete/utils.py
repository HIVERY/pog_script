
import re
import logging
import enum
from decimal import Decimal, ROUND_HALF_UP
from itertools import tee
import copy

logger = logging.getLogger(__name__)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def parse_float(val, default=None):
    """Try to parse str value to float"""
    return parse_num(val, float, r'[-+]?\d*\.\d+|\d+', 1, default)


def parse_int(val, default=None):
    """Try to parse str value to int."""
    return parse_num(val, int, r'[-+]?\d+', 1, default)


def parse_num(val, type_, pattern, max_matches, default=None):
    """
    Try to conver stirng value [val] to numeric type [type_]. If
    unsuccessfull use fallback regex pattern to parse string into
    numeric representation and then convert to the type specified.
    If max_matches > 1 will try to parse more than 1 regex match in a
    string and return a list of converted values.
    If conversion unsuccessfull return default value.
    """
    if not val or len(str(val).strip()) == 0:
        return default

    try:
        return type_(val)
    except ValueError:
        # logger.warning('Default conversion to {} failed. Using fallback.'
        #                .format(str(type_)))
        try:
            s = get_matches(val, pattern, max_matches)
            if len(s) == 0:
                logger.warning('No {} found in {}'.format(str(type_), val))
            return type_(s[0])
        except Exception:
            logger.exception('Failed to convert {} to {}'
                             .format(val, str(type_)))
            return default
    except Exception:
        logger.exception('Failed to convert {} to {}'.format(val, str(type_)))


def get_matches(s, pattern, max_number=None):
    """
    Return mathes of regex pattern in a string. If max_number is
    set to not None, return subset of matches equals to max_number.
    """

    if not isinstance(s, str):
        s = str(s)

    matches = re.findall(pattern, s)
    if max_number is None or len(matches) <= max_number:
        return matches
    return matches[:max_number]


def get_uom_from_str(unit_str):
    unit_str = unit_str.lower().strip()
    if unit_str in ['fl oz', 'fl. oz.', 'fl. oz', 'fl oz.', 'oz', 'oz.',
                    'ounce', 'ounces']:
        return UnitOfMeasure.oz
    elif unit_str in ['ml', 'millilitre', 'milliliter', 'mililiter']:
        return UnitOfMeasure.ml
    elif unit_str in ['l', 'litre', 'liter']:
        return UnitOfMeasure.l
    else:
        # logger.error("Unit String {} not recognised.".format(unit_str))
        return UnitOfMeasure.unknown


class UnitOfMeasure(enum.Enum):
    oz = "oz"
    ml = "ml"
    l = "l"
    unknown = "unknown"


class ReadData:
    """
    A class to abstract the reading of data from either a string or a file
    """

    def __init__(self, f=None, encoding='utf8', as_lines=False):
        self.f = f
        # self.f_str = f_str
        self.file = None
        self.encoding = encoding
        self.as_lines = as_lines

    def __enter__(self):
        # if self.f_str:
        #     return self.f_str.splitlines()
        if self.f:
            if self.as_lines:
                with open(self.f, 'rt', encoding=self.encoding) as file:
                    return file.readlines()
            else:
                self.file = open(self.f, 'rt', encoding=self.encoding)
                return self.file

    def __exit__(self, type, value, traceback):
        if self.file:
            # If it was a file close it
            self.file.close()


def compare_floats(float1, compare_operator, float2, number_of_decimals=2, rounding=ROUND_HALF_UP):
    # Deal with infinity
    if float1 > 1e25:
        float1 = 1e25
    if float2 > 1e25:
        float2 = 1e25
    decimal1 = Decimal(float1).quantize(Decimal(str(10 ** -number_of_decimals)), rounding)
    decimal2 = Decimal(float2).quantize(Decimal(str(10 ** -number_of_decimals)), rounding)
    if compare_operator == '==':
        return decimal1 == decimal2
    if compare_operator == '!=':
        # print(decimal1, decimal2)
        return decimal1 != decimal2
    elif compare_operator == '<=':
        return decimal1 <= decimal2
    elif compare_operator == '>=':
        return decimal1 >= decimal2
    elif compare_operator == '<':
        return decimal1 < decimal2
    elif compare_operator == '>':
        return decimal1 > decimal2
    else:
        raise ValueError("Unknown comparison operator: {}".format(compare_operator))


def can_combine(shelf1, shelf2):
    # needs same y-coordinate
    if compare_floats(round(shelf1.coordinate_y, 2), "!=", round(shelf2.coordinate_y, 2)):
        error = f'coordinate_y {round(shelf1.coordinate_y,2)}, {round(shelf2.coordinate_y,2)} is not some'
        return False, error
    if compare_floats(shelf1.shelf_depth, "!=", shelf2.shelf_depth):                # needs same depth
        error = f'shelf_depth {shelf1.shelf_depth}, {shelf2.shelf_depth} is not some'
        return False, error
    if compare_floats(shelf1.shelf_slope, "!=", shelf2.shelf_slope):                # needs same slope
        error = f'shelf_slope {shelf1.shelf_slope}, {shelf2.shelf_slope} is not some'
        return False, error
    if compare_floats(shelf1.coordinate_x + shelf1.shelf_width, "!=", shelf2.coordinate_x):        # needs to be adjacent
        error = f'coordinate_x not adjacent {shelf1.coordinate_x + shelf1.shelf_width }, {shelf2.coordinate_x} is not some, will split the shelves'
        return False, error
    return True, ''


def validate_combined_shelves(combined_shelves):
    fail = False
    new_combined_shelves = copy.deepcopy(combined_shelves)
    if not combined_shelves:
        raise Exception('combine shelves is not created')
    for idx1, CombinedShelves in enumerate(combined_shelves):
        for idx2, combinedShelf in enumerate(CombinedShelves):
            if len(combinedShelf) == 1:
                continue
            for i in range(len(combinedShelf)-1):
                combine, error = can_combine(combinedShelf[i], combinedShelf[i+1])
                if combine:
                    continue
                else:
                    fail = True
                    del new_combined_shelves[idx1][idx2]  
                    new_combined_shelves[idx1].extend([combinedShelf[:i+1], combinedShelf[i+1:]])
                    logger.warning(f'validate failed: can not combine cause {error}')
    return new_combined_shelves, fail


def dynamicCombine(lis):
    """ using DP and pruning to find all the combinations
    Args:
        lis ([Miniplanogram object]): [shelf with combination options]

    Returns:
        list[list]: [all the combinations of one layer]
    
    for example:
        one layer shelf with combine flag
            ['NO,"RIGHT",'BOTH','RIGHT','NO','LEFT', 'RIGHT', 'RIGHT']
        
        return all possible combinations if it can combine together
           [['NO'], ["RIGHT", 'BOTH'], ['RIGHT'], ['NO'], ['LEFT'], ['RIGHT'], ['RIGHT']]
    """
    comb = []
    if len(lis) == 1:
        return [lis]
    while lis and lis[0].combine_direction in ['NO', 'LEFT']:
        comb.append([lis[0]])
        lis.pop(0)
    if len(lis) == 1:
        comb.append([lis[0]]) 
        return comb
    if not lis:
        return comb
    dp = [0] * len(lis)
    
    # init DP list
    dp[0] = [lis[0]]
    # init Pruning list
    prune = [1] * len(lis)

    for i in range(1, len(lis)):
        if lis[i].combine_direction == "NO":
            if prune[i-1]:
                comb.append(dp[i-1])
                prune[i-1] = 0
            if len(dp[i-1]) != 1 or (len(dp[i-1]) >= 1 and dp[i-1][-1].combine_direction != 'NO'):
                prune[i] = 0
                comb.append([lis[i]])
            dp[i] = [lis[i]]
            if prune[i]:
                comb.append(dp[i])
                prune[i] = 0
        if dp[i-1][-1].combine_direction in ["RIGHT", "BOTH"] and lis[i].combine_direction == 'BOTH':
            dp[i] = dp[i-1] + [lis[i]]
            if i == len(lis) - 1:
                comb.append(dp[i])
        if dp[i-1][-1].combine_direction in ["RIGHT", "BOTH"] and lis[i].combine_direction == 'LEFT':
            dp[i] = dp[i-1] + [lis[i]]
            if prune[i]:
                comb.append(dp[i])
                prune[i] = 0
        if dp[i - 1][-1].combine_direction in ['LEFT', 'NO']:
            dp[i] = [lis[i]]
            if i == len(lis) - 1 and prune[i]:
                comb.append(dp[i])
                prune[i] = 0
        if dp[i-1][-1].combine_direction in ['LEFT', 'NO'] and lis[i].combine_direction == 'LEFT':
            if prune[i]:
                comb.append([lis[i]])
                prune[i] = 0
        if dp[i-1][-1].combine_direction in ["RIGHT", "BOTH"] and lis[i].combine_direction == 'RIGHT':
            dp[i] = [lis[i]]
            if prune[i-1]:
                comb.append(dp[i-1])
                prune[i-1] = 0
        if i == len(lis) - 1 and lis[i].combine_direction == 'RIGHT' and prune[i]:
            comb.append([lis[i]])
    return comb
