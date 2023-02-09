# CMAPD solution cost regression
This code tries to predict the cost of a conflict free solution
for a CMAPD instance (with already assigned tasks) using regression.
The best $R^2$ score achieved so far is 0.97!

### Usage
How to train the model:
1. change the value of the configuration variables in `config.py`
2. run `python datasetGenerator.py` to generate the dataset based on the config variables.
3. run `python train.py` to train the model.

The trained model will also be saved for later usage. 
