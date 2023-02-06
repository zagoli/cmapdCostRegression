# Jacopo Zagoli, 30/01/2023
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.dummy import DummyRegressor
from config import *
import numpy as np

if __name__ == '__main__':
    assert FEATURES_FILE_PATH.exists(), 'Cannot find features file.'
    csv_data = np.genfromtxt(FEATURES_FILE_PATH, delimiter=',')
    X, Y = csv_data[:, :-1], csv_data[:, -1]

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, shuffle=False)
    model = XGBRegressor()
    dummy = DummyRegressor()
    model.fit(X_train, Y_train)
    dummy.fit(X_train, Y_train)
    Y_hat = model.predict(X_test)
    Y_hat_dummy = dummy.predict(X_test)
    mse = mean_squared_error(Y_test, Y_hat)
    mse_dummy = mean_squared_error(Y_test, Y_hat_dummy)

    print(f'{"Dummy MSE:":10s} {mse_dummy:10.5f}')
    print(f'{"Real MSE:":10s} {mse:10.5f}')
    proceed = input('Do you want to train the model on all data and save it? y/n: ').upper() == 'Y'
    if proceed:
        model.fit(X, Y)
        model.save_model(MODEL_FILE_PATH)
        print('Model saved.')
