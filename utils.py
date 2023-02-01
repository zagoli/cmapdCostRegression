# Jacopo Zagoli, 31/01/2023
import numpy as np


def ravel(point, n_cols):
    return point[0] * n_cols + point[1]


def read_map(map_path):
    with open(map_path) as f:
        grid_size = tuple(map(int, f.readline().strip().split(',')))
        grid = np.genfromtxt(map_path, delimiter=1, skip_header=1, dtype='S')
    return grid, grid_size
