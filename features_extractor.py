# Jacopo Zagoli, 31/01/2023
from utils import ravel
from grid_solver import GridSolver


class FeaturesExtractor:

    def __init__(self, assignment: list, grid, grid_size: tuple, grid_solver: GridSolver):
        self.__assignment = assignment
        self.__grid = grid
        self.__grid_size = grid_size
        self.__grid_solver = grid_solver
        self.__paths = self.__compute_paths()
        self.__conflicts = self.__compute_conflicts()

    def __get_agents_start_goal(self):
        n_cols = self.__grid_size[1]
        locations = []
        for waypoints in self.__assignment:
            locations += [waypoints[0], waypoints[-1]]
        return [ravel(p, n_cols) for p in locations]

    def get_features(self):
        features = []
        features += self.__get_agents_start_goal()
        return features

    def __compute_paths(self):
        paths = []
        for waypoints in self.__assignment:
            path = self.__grid_solver.get_waypoints_path(waypoints)
            paths.append(path)
        return paths

    def __compute_conflicts(self):
        raise NotImplementedError()
