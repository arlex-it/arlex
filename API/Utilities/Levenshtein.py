import numpy as np
from difflib import SequenceMatcher


def levenshtein_distance(str_one, str_two):
    size = [len(str_one), len(str_two)]
    matrix = np.zeros((size[0], size[1]))

    # matrix initialization
    for i in range(len(str_one)):
        matrix[i, 0] = i
    matrix[0] = [j for j in range(len(str_two))]

    for i in range(1, size[0]):
        for j in range(1, size[1]):
            subs = 0 if str_one[i-1] == str_two[j-1] else 1
            matrix[i, j] = min(
                matrix[i-1, j] + 1,
                matrix[i-1, j-1] + subs,
                matrix[i, j-1] + 1
            )
    return matrix[size[0]-1, size[1]-1]


def calc_similarity(name, asked):
    return SequenceMatcher(None, name, asked).ratio()
