# Jacopo Zagoli, 27/01/2023
import grid_solver
from config import *
import os
import csv
import joblib
import numpy as np
from oracle.oracle import oracle  # PyCharm doesn't find it but it's there
from utils import ravel, read_grid
from features_extractor import FeaturesExtractor
from grid_solver import GridSolver


def format_grid_for_oracle(grid):
    return grid.ravel() == b'@'


def format_waypoints_for_oracle(waypoints, n_cols):
    sep = np.array(list(map(len, waypoints)), dtype=np.int32)
    waypoints = np.array([ravel(p, n_cols) for a in waypoints for p in a], dtype=np.int32)
    return sep, waypoints


def call_oracle(waypoints, grid, grid_size):
    num_agents = len(waypoints)
    row, col = grid_size
    sep, waypoints = format_waypoints_for_oracle(waypoints, col)
    cost = oracle(grid, waypoints, sep, num_agents, len(waypoints), row, col)
    return int(np.rint(cost))


if __name__ == '__main__':
    assert GRID_PATH.exists(), 'Cannot find the grid file.'
    assert ASSIGNMENTS_DIRECTORY.exists(), 'Cannot find assignments directory.'
    assignment_names = os.listdir(ASSIGNMENTS_DIRECTORY)
    grid, grid_size = read_grid(GRID_PATH)
    grid_solver = GridSolver(grid)
    oracle_grid = format_grid_for_oracle(grid)
    with open(FEATURES_FILE_PATH, 'w', encoding='UTF8') as features_file:
        writer = csv.writer(features_file)
        for assignment_name in assignment_names:
            assignment = joblib.load(ASSIGNMENTS_DIRECTORY / str(assignment_name))
            extractor = FeaturesExtractor(assignment, oracle_grid, grid_size, grid_solver)
            extracted_features = extractor.get_features()
            solution = call_oracle(assignment, oracle_grid, grid_size)
            extracted_features.append(solution)
            writer.writerow(extracted_features)
