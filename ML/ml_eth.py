# librairies
import pandas as pd
import numpy as np
import joblib
import mlflow.sklearn
from mlflow import MlflowClient 
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from backtest import backtest_strategy, buy_and_hold_strategy

# MLflow tracking_uri
client = MlflowClient(tracking_uri="http://127.0.0.1:8080")

random_state = 10

# Define experiment name, run name and artifact_path name
eth_rf_regressor = mlflow.set_experiment("ETH_RandomForestRegressor")
run_name = f"{random_state}_run"
artifact_path = "eth_rfr"

# chargement des données
eth = pd.read_parquet("data/eth_1h")

# Création des colonnes qu'on estimera
eth["in_1_hour"] = eth["close"].shift(-1)
eth = eth[:-1]  # on supprime la dernière ligne

# divisions des données en 'feats' et 'target"
feats = eth[['open', 'high', 'low', 'close', 'volume', 'trades']]
target = eth["in_1_hour"]

# on sépare les données avec une date
train_date, test_date = "2023-12-30", "2024-01-01"
X_train, X_test = feats.loc[:train_date], feats[test_date:]
y_train, y_test = target[:train_date], target[test_date:]

# Normalisation des caractéristiques
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# paramètres
params = {
    "random_state": random_state,
}

# entrainement du modèle
rfr = RandomForestRegressor(**params)
rfr.fit(X_train_scaled, y_train)

# évaluation du modèle
y_pred = rfr.predict(X_test_scaled) # prédiction
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)
# backtest metrics
investment = 10000
# btc_rfr_total_value = backtest_strategy(model=rfr, X_test_scaled=X_test_scaled, y_test=y_test, initial_cash=investment, task="regression")
model_return_percentage = ((backtest_strategy(model=rfr, X_test_scaled=X_test_scaled, y_test=y_test, initial_cash=investment, task="regression")[-1]) - investment) / investment
refernce_return_percentage = (buy_and_hold_strategy(y_test=y_test, initial_cash=investment) - investment) / investment

metrics = {
  "mae": mae,
  "mse": mse,
  "rmse": rmse,
  "r2": r2,
  "model_return_percentage": model_return_percentage,
  "refernce_return_percentage": refernce_return_percentage
}

# Store information in tracking server
with mlflow.start_run(run_name=run_name) as run:
  # Enregistrement des hyperparamètres par défaut
  params = rfr.get_params()
  for param, value in params.items():
      mlflow.log_param(param, value)
  mlflow.log_metrics(metrics)
  mlflow.sklearn.log_model(
    sk_model=rfr,
    input_example=X_test_scaled,
    artifact_path=artifact_path
  )

  print(f"Model saved in run {mlflow.active_run().info.run_uuid}")

# Enregistrement le scaler avec joblib
joblib.dump(scaler, "models/eth_scaler")
# Enregistrement du modèle avec joblib
joblib.dump(rfr, "models/eth_model")
