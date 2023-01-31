# Jacopo Zagoli, 31/01/2023
from utils import ravel


class FeaturesExtractor:

    def __init__(self, assignment, grid, grid_size):
        self.__assignment = assignment
        self.__grid = grid
        self.__grid_size = grid_size

    def get_agents_start_goal(self):
        n_cols = self.__grid_size[1]
        locations = []
        for waypoints in self.__assignment:
            locations += [waypoints[0], waypoints[-1]]
        return [ravel(p, n_cols) for p in locations]
