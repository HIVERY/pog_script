from itertools import tee
import re
import logging
import enum
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


def dynamicCombine(lis):
    ll = copy.deepcopy(lis)
    comb = []
    if lis[0].combine_direction == 'NO' or lis[0].combine_direction == 'LEFT':
        comb.append([lis[0]])
        lis.pop(0)
    dp = [0] * len(lis)
    dp[0] = [lis[0]]
    prune = [1] * len(lis)
    for i in range(1, len(lis)):
        # print(comb)
        if lis[i].combine_direction == "NO":
            if prune[i-1]:
                comb.append(dp[i-1])
                prune[i-1] = 0
            if len(dp[i-1]) != 1 and dp[i-1][-1].combine_direction != 'NO':
                comb.append([lis[i]])
            dp[i] = [lis[i]]
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
            if i == len(lis) - 1:
                comb.append(dp[i])
        if dp[i-1][-1].combine_direction in ['LEFT', 'NO'] and lis[i].combine_direction == 'LEFT':
            comb.append([lis[i]])
        if dp[i-1][-1].combine_direction in ["RIGHT", "BOTH"] and lis[i].combine_direction == 'RIGHT':
            dp[i] = [lis[i]]
            if prune[i-1]:
                comb.append(dp[i-1])
                prune[i-1] = 0
        if i == len(lis) - 1 and lis[i].combine_direction == 'RIGHT':
            comb.append([lis[i]])
    # input(lis)
    # # print(comb)
    # print([v for k in comb for v in k])
    print([v for k in comb for v in k] == ll)
    # k = [v for k in comb for v in k]
    # for i in range(len(k)):
    #     print(k[i])
    #     print(k[i] == lis[i])
    return comb