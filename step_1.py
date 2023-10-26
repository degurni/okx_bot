
import yfinance as yf
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from math import sqrt
from sklearn.metrics import mean_squared_error
import warnings





google = yf.Ticker('GOOG')

df =google.history(period='1d', interval='1m')

df['Date'] = pd.to_datetime(df.index).time
df.set_index('Date', inplace=True)

def evaluate_arima_model(X, arima_order):
    train_size = int(len(X) * 0.66)
    train, test = X[0:train_size], X[train_size:]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=arima_order).fit()
        yhat = model.forecast(steps=1)[0]
        predictions.append(yhat)
        history.append(test[t])
    rmse = sqrt(mean_squared_error(test, predictions))
    return rmse

def evaluate_models(dataset, p_values, d_values, q_values):
    best_score, best_cfg = float('inf'), None
    for p in p_values:
        for d in d_values:
            for q in q_values:
                order = (p, d, q)
                try:
                    rmse = evaluate_arima_model(dataset, order)
                    if rmse < best_score:
                        best_score, best_cfg = rmse, order
                    print(f'ARIMA-{order} RMSE-{round(rmse, 3)}')
                except:
                    continue

    print(f'Лучший ARIMA-{best_cfg} RMSE-{round(best_score, 3)}')


p_values = [0, 1, 2, 4, 6, 8, 10]
d_values = range(0, 3)
q_values = range(0, 3)

warnings.filterwarnings('ignore')
evaluate_models(df.Close.values, p_values, d_values, q_values)

"""
ARIMA-(0, 1, 0) RMSE-0.076
ARIMA-(0, 1, 1) RMSE-0.076
ARIMA-(0, 1, 2) RMSE-0.076
"""
