# Jacopo Zagoli, 30/01/2023
from xgboost import XGBRegressor
from sklearn.model_selection import cross_val_score
from config import *
import numpy as np

if __name__ == '__main__':
    assert FEATURES_FILE_PATH.exists(), 'Cannot find features file.'

    csv_data = np.genfromtxt(FEATURES_FILE_PATH, delimiter=',')
    X, Y = csv_data[:, :-1], csv_data[:, -1]

    #Best score:  0.9743085405338278
    #Best params:  {'learning_rate': 0.001, 'max_depth': 10, 'n_estimators': 10000}
    model = XGBRegressor(n_estimators=10_000, max_depth=10, learning_rate=0.001)

    scores = cross_val_score(model, X, Y, cv=5, verbose=2)
    print(f'The mean R2 score is {scores.mean()} with a standard deviation of {scores.std()}')

    proceed = input('Do you want to train the model on all data and save it? y/n: ').upper() == 'Y'
    if proceed:
        model.fit(X, Y, verbose=2)
        model.save_model(MODEL_FILE_PATH)
        print('Model saved.')
