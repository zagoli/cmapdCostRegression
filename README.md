# C-Mapd solution cost regression
This code tries to predict the cost of a conflict free
solution of a C-Mapd instance (with already assigned tasks)
using regression.

### Usage
How to train the model:
1. change the value of the configuration variables in `config.py`
2. run `python waypointsGenerator.py` to generate the desired number of assignments.
3. run `python featuresExtraxtor.py` to generate the actual dataset based on the previously generated assignments.
4. run `python train.py` to train the model.

The trained model will also be saved for later usage. 