# Jacopo Zagoli, 27/01/2023
from pathlib import Path
from config import *
import os
import csv
import joblib
import numpy as np
from oracle.oracle import oracle


def read_map_for_oracle(map_path):
    with open(map_path) as f:
        grid_size = tuple(map(int, f.readline().strip().split(',')))
        grid = np.genfromtxt(map_path, delimiter=1, skip_header=1, dtype='S').ravel() == b'@'
    return grid, grid_size


def extract_features(ass):
    return [1, 2, 3, 4]


def format_waypoints_for_oracle(ass, grid_size):
    sep = np.array(list(map(len, ass)), dtype=np.int32)
    waypoints = np.array([p[0] * grid_size[1] + p[1] for a in ass for p in a], dtype=np.int32)
    return sep, waypoints


def call_oracle(ass, grid, grid_size):
    num_agents = len(ass)
    sep, waypoints = format_waypoints_for_oracle(ass, grid_size)
    row, col = grid_size
    cost = oracle(grid, waypoints, sep, num_agents, len(waypoints), row, col)
    return int(np.rint(cost))


if __name__ == '__main__':
    assert MAP_PATH.exists(), 'Cannot find the map file.'
    assert ASSIGNMENTS_DIRECTORY.exists(), 'Cannot find assignments directory.'
    assignments_list = os.listdir(ASSIGNMENTS_DIRECTORY)
    oracle_map, oracle_map_size = read_map_for_oracle(MAP_PATH)
    with open(FEATURES_FILE_PATH, 'w', encoding='UTF8') as features_file:
        writer = csv.writer(features_file)
        for pickled_assignment in assignments_list:
            assignment = joblib.load(ASSIGNMENTS_DIRECTORY / str(pickled_assignment))
            features = extract_features(assignment)
            solution = call_oracle(assignment, oracle_map, oracle_map_size)
            features.append(solution)
            writer.writerow(features)
