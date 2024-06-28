# import libraries
import pandas as pd
from sqlalchemy import create_engine

# Example: 'postgresql://username:password@localhost:5432/your_database'
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
adress = os.getenv("DB_ADRESS")
#address = os.environ['DB_ADDRESS']

conn_string = f"postgresql://{user}:{password}@{adress}:5432/data_binance"

print (' connexion à la base de donnees')

# Connexion avec sqlalchemy
engine = create_engine(conn_string)

# notre requête
query = "SELECT * FROM historical_klines WHERE timestamp <= '2024-04-30' ORDER BY timestamp ASC"

# récupération des données
data = pd.read_sql(query, engine)

# transformation du temps en index
data = data.set_index(data["timestamp"])
del data["timestamp"] # suppression de la colonne

# séparation des données dans les df différents
btc = data[data["symbol"] == "BTCUSDT"]
eth = data[data["symbol"] == "ETHUSDT"]
bnb = data[data["symbol"] == "BNBUSDT"]
sol = data[data["symbol"] == "SOLUSDT"]
xrp = data[data["symbol"] == "XRPUSDT"]

# suppression de la colonne 'symbol'
del btc["symbol"]
del eth["symbol"]
del bnb["symbol"]
del sol["symbol"]
del xrp["symbol"]

# sauvegarde des données
btc.to_parquet("ML/data/btc_1h")
eth.to_parquet("ML/data/eth_1h")
bnb.to_parquet("ML/data/bnb_1h")
sol.to_parquet("ML/data/sol_1h")
xrp.to_parquet("ML/data/xrp_1h")