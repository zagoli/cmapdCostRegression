# Jacopo Zagoli, 31/01/2023
from utils import ravel
from grid_solver import GridSolver
from conflicts import ConflictsFinder


class FeaturesExtractor:

    def __init__(self, assignment: list, grid, grid_size: tuple, grid_solver: GridSolver):
        self.__assignment = assignment
        self.__grid = grid
        self.__grid_size = grid_size
        self.__grid_solver = grid_solver
        self.__paths = self.__compute_paths()
        self.__conflicts = self.__compute_conflicts()

    def __compute_paths(self):
        paths = []
        for waypoints in self.__assignment:
            path = self.__grid_solver.get_waypoints_path(waypoints)
            paths.append(path)
        return paths

    def __compute_conflicts(self):
        finder = ConflictsFinder(self.__paths)
        return finder.get_conflicts()

    def get_features(self):
        features = []
        features += self.__agents_start_goal()
        features += self.__n_waypoints_per_agent()
        features += self.__paths_length()
        features += self.__n_conflicts()
        return features

    def __agents_start_goal(self) -> list:
        n_cols = self.__grid_size[1]
        locations = []
        for waypoints in self.__assignment:
            locations += [waypoints[0], waypoints[-1]]
        return [ravel(p, n_cols) for p in locations]

    def __n_waypoints_per_agent(self) -> list:
        return [len(waypoints) for waypoints in self.__assignment]

    def __paths_length(self) -> list:
        return [len(path) for path in self.__paths]

    def __n_conflicts(self) -> list:
        return [len(self.__conflicts)]
