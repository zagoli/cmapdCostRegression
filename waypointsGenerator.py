# Jacopo Zagoli, 26/01/2023
from numpy.random import default_rng
from pathlib import Path
import numpy as np
import random
import copy
import joblib

class MapPointsGenerator:
    def __init__(self, map_path):
        self.original_points = available_map_points(map_path)
        self.points = None
        self.reset()
    def get_point(self):
        point = random.choice(self.points)
        self.points.remove(point)
        return point
    def get_points(self, n_points):
        point_list = []
        for _ in range(n_points):
            point_list.append(self.get_point())
        return point_list
    def reset(self):
        self.points = copy.deepcopy(self.original_points)


def available_map_points(map_path):
    available_points = []
    with open(map_path) as f:
        lines = f.readlines()
    del lines[0]
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == 'e':
                available_points.append([row, col])
    return available_points


def tasks_per_agent(n_agents, n_tasks):
    mean_tasks_per_agent = n_tasks // n_agents
    std = mean_tasks_per_agent / 3
    rng = default_rng()
    tasks_number_list = rng.normal(loc=mean_tasks_per_agent, scale=std, size=n_agents)
    tasks_number_list = np.rint(tasks_number_list).astype(int)
    while np.sum(tasks_number_list) > n_tasks:
        largest = np.argmax(tasks_number_list)
        tasks_number_list[largest] -= 1
    while np.sum(tasks_number_list) < n_tasks:
        smallest = np.argmin(tasks_number_list)
        tasks_number_list[smallest] += 1
    return tasks_number_list


def generate_assignments(n_agents, n_tasks, point_generator):
    tasks_number = tasks_per_agent(n_agents, n_tasks)
    assignment_list = []
    for agent in range(n_agents):
        # add starting point
        assignment = [point_generator.get_point()]
        # add points for tasks
        assignment += point_generator.get_points(tasks_number[agent])
        assignment_list.append(assignment)
    return assignment_list


if __name__ == '__main__':
    AGENTS = 10
    TASKS = 20
    NUMBER_OF_ASSIGNMENTS = 10
    MAP_PATH = Path('env/grid.map')
    SAVE_PATH = Path('assignments')

    SAVE_PATH.mkdir(exist_ok=True)
    map_points = MapPointsGenerator(MAP_PATH)

    for ass_number in range(NUMBER_OF_ASSIGNMENTS):
        assignments = generate_assignments(AGENTS, TASKS, map_points)
        filename = SAVE_PATH / ('assignment_' + str(ass_number) + '.pkl')
        joblib.dump(assignments, filename)
        map_points.reset()