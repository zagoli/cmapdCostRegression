from pathlib import Path

NUMBER_OF_ASSIGNMENTS = 10_000 # The number of assignments that will be generated for training
AGENTS = 10 # The number of agents in the assignments
TASKS = 20 # The number of tasks to be assigned to the agents
ASSIGNMENTS_DIRECTORY = Path('assignments') # Where the assignments will be saved
GRID_PATH = Path('env/grid.map') # The path to the grid
FEATURES_FILE_PATH = Path('features.csv') # Where the dataset will be saved
MODEL_FILE_PATH = Path('model.json') # Where the model will be saved
