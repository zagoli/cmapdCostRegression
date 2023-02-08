# Jacopo Zagoli, 26/01/2023
from tqdm import tqdm
from numpy.random import default_rng
from config import *
from utils import read_grid
import numpy as np
import random
import copy
import joblib

class GridPointsGenerator:
    def __init__(self, grid_path):
        self.__grid_path = grid_path
        self.__original_points = self.__available_grid_points()
        self.__points = None
        self.reset()
    def get_point(self):
        point = random.choice(self.__points)
        self.__points.remove(point)
        return point
    def get_points(self, n_points):
        point_list = []
        for _ in range(n_points):
            point_list.append(self.get_point())
        return point_list
    def reset(self):
        self.__points = copy.deepcopy(self.__original_points)
    def __available_grid_points(self):
        available_points = []
        grid, grid_size = read_grid(self.__grid_path)
        for row in range(grid_size[0]):
            for col in range(grid_size[1]):
                if grid[row, col] == b'e':
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


def generate_assignment(n_agents, n_tasks, point_generator):
    tasks_number = tasks_per_agent(n_agents, n_tasks)
    assignment_list = []
    for agent in range(n_agents):
        # add starting point
        assignment = [point_generator.get_point()]
        # add points for tasks
        assignment += point_generator.get_points(tasks_number[agent])
        assignment_list.append(assignment)
    return assignment_list


def generate_assignments(assignments_number, grid_path):
    grid_points = GridPointsGenerator(grid_path)
    for ass_number in range(assignments_number):
        assignment = generate_assignment(AGENTS, TASKS, grid_points)
        yield assignment
        grid_points.reset()