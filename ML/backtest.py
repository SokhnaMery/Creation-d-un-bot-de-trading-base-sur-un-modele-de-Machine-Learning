# librairies
import pandas as pd

# Fonction pour backtester le modèle
def backtest_strategy(model, X_test_scaled, y_test, initial_cash=10000, task='regression'):
    cash = initial_cash
    holdings = 0
    total_value = []
    for i in range(len(X_test_scaled)):
        X_sample = X_test_scaled[i].reshape(1, -1)
        if task == 'regression':
            prediction = model.predict(X_sample)[0]
            actual_price = y_test.iloc[i]
            if prediction > actual_price:
                # Buy signal
                holdings += cash / actual_price
                cash = 0
            elif prediction < actual_price and holdings > 0:
                # Sell signal
                cash += holdings * actual_price
                holdings = 0
        else:
            prediction = model.predict(X_sample)[0]
            actual_price = y_test.iloc[i]
            if prediction == 1:
                # Buy signal
                holdings += cash / actual_price
                cash = 0
            elif prediction == 0 and holdings > 0:
                # Sell signal
                cash += holdings * actual_price
                holdings = 0
        total_value.append(cash + holdings * actual_price)
    return total_value

def buy_and_hold_strategy(y_test, initial_cash=10000):
    # Acheter au début de la période de test
    initial_price = y_test.iloc[0]
    holdings = initial_cash / initial_price
    # Vendre à la fin de la période de test
    final_price = y_test.iloc[-1]
    final_value = holdings * final_price
    return final_value