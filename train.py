# Jacopo Zagoli, 30/01/2023
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from pathlib import Path
import numpy as np

if __name__ == '__main__':
    FEATURES_FILE = Path('features.csv')
    MODEL_FILE_NAME = Path('model.json')

    assert FEATURES_FILE.exists(), 'Cannot find features file.'
    csv_data = np.genfromtxt(FEATURES_FILE, delimiter=',')
    X, Y = csv_data[:, :-1], csv_data[:, -1]

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y)
    model = XGBRegressor()
    model.fit(X_train, Y_train)
    Y_hat = model.predict(X_test)
    mse = mean_squared_error(Y_test, Y_hat)

    print(f'The mean square error is: {mse}.')
    proceed = input('Do you want to train the model on all data and save it? y/n: ').upper() == 'Y'
    if proceed:
        model.fit(X, Y)
        model.save_model(MODEL_FILE_NAME)
        print('Model saved.')
