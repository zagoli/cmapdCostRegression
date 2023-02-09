# CMAPD solution cost regression
This code tries to predict the cost of a conflict free solution
for a CMAPD instance (with already assigned tasks) using regression.
The best $R^2$ score achieved so far is 0.97!

### Installation
Installation instructions for Linux and similar systems:
1. create a conda environment with the provided requirements file: `conda_env_requirements.txt`;
2. clone this repo;
3. activate the environment and navigate to `cmapdCostRegression/oracle`;
4. run `make`.
All done!

### Usage
How to train the model:
1. change the value of the configuration variables in `config.py` if needed;
2. run `python datasetGenerator.py` to generate the dataset based on the config variables;
3. run `python train.py` to train the model.

The trained model will also be saved for later usage. 
