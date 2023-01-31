# Jacopo Zagoli, 27/01/2023
from config import *
import os
import csv
import joblib
import numpy as np
from oracle.oracle import oracle  # PyCharm doesn't find it but it's there
from utils import ravel
from features_extractor import FeaturesExtractor


def read_map_for_oracle(map_path):
    with open(map_path) as f:
        grid_size = tuple(map(int, f.readline().strip().split(',')))
        grid = np.genfromtxt(map_path, delimiter=1, skip_header=1, dtype='S').ravel() == b'@'
    return grid, grid_size


def features_composer(features_extractor):
    features = []
    features += features_extractor.get_agents_start_goal()
    return features


def format_waypoints_for_oracle(waypoints, grid_size):
    sep = np.array(list(map(len, waypoints)), dtype=np.int32)
    waypoints = np.array([ravel(p, grid_size) for a in waypoints for p in a], dtype=np.int32)
    return sep, waypoints


def call_oracle(waypoints, grid, grid_size):
    num_agents = len(waypoints)
    sep, waypoints = format_waypoints_for_oracle(waypoints, grid_size)
    row, col = grid_size
    cost = oracle(grid, waypoints, sep, num_agents, len(waypoints), row, col)
    return int(np.rint(cost))


if __name__ == '__main__':
    assert MAP_PATH.exists(), 'Cannot find the map file.'
    assert ASSIGNMENTS_DIRECTORY.exists(), 'Cannot find assignments directory.'
    assignment_names = os.listdir(ASSIGNMENTS_DIRECTORY)
    oracle_map, oracle_map_size = read_map_for_oracle(MAP_PATH)
    with open(FEATURES_FILE_PATH, 'w', encoding='UTF8') as features_file:
        writer = csv.writer(features_file)
        for assignment_name in assignment_names:
            assignment = joblib.load(ASSIGNMENTS_DIRECTORY / str(assignment_name))
            extractor = FeaturesExtractor(assignment, oracle_map, oracle_map_size)
            extracted_features = features_composer(extractor)
            solution = call_oracle(assignment, oracle_map, oracle_map_size)
            extracted_features.append(solution)
            writer.writerow(extracted_features)