from fastapi import FastAPI
from fastapi import Header
from sklearn.preprocessing import StandardScaler
api = FastAPI(
    title="OPA Bot Trading",
    description="My own API for bot trading powered by FastAPI.",
    version="1.0.1")

@api.get('/', name = 'OPA: BOT - Crypto')
def get_index():
    """
    Welcome on OPA bot trading for cryptocurrencies
    """
    return {'Message': 'Welcome on OPA bot trading for cryptocurrencies'}

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import joblib
import requests

class Kline(BaseModel):
    """
    informations on cryptocurrency hour kline
    """
    Open : float
    High : float
    Low : float
    Close : float
    Volume : float
    Trades : float


@api.get('/kline infor', name='Get hour Kline information for cryptocurrency in a day')
def get_kline_info(crypto_currency: str = Header(None, description='symbol of cryptocurrency'), the_day: str = Header(None, description = 'Day concerned')):
    """
    Select and display informations for a cryptocurrency klines on a day
    Enter a symbol for cryptocurrencies between the following : BTCUSDT, ETHUSDT , BNBUSDT, SOLUSDT, XRPUSDT
    Enter the day in the format : 'YYYY-MM-DD' example 2027-08-17
    """
    # connection string for the database =  'postgresql://username:password@localhost:5432/your_database'
    # Connection à la base des données Posgresql sur le cloud
    # Récupération des informations de connexion à partir des variables d'environnement
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    adress = os.getenv("DB_ADDRESS")
    conn_string = f"postgresql://{user}:{password}@{adress}:5432/database_binance"

    # Connexion with psycopg2
    conn = psycopg2.connect(conn_string)

    # Open a cursor to perform database operations
    cursor = conn.cursor()
    #query to select klines for cryptocurrency  on day given in paramters
    query = "SELECT Timestamp, Open, High, Low, Close, Volume, Trades FROM historical_klines where symbol = '"+ crypto_currency+"' and TO_CHAR(timestamp, 'YYYY-MM-DD')= '"+ the_day +"' ORDER BY timestamp ASC"
    cursor.execute(query)
    data = pd.read_sql_query(query, conn)
    list_kline_infos =[]
    pos =0
    while pos <len(data):
        print('iteration ',pos+1,' de la boucle  while')
        elt = data.values[pos]
        list_kline_infos.append(('Timestamp: ', elt[0], 'Open: ' , elt[1], 'High: ' ,elt[2], 'Low: ' , elt[3], 'Close: ' ,elt[4], 'Volume: ' , elt[5], 'Trades: ' ,elt[6]))
        pos +=1
    return {
        'Klines informations for': crypto_currency,
        'Date' : the_day,
        'Datas' : list_kline_infos
    }

@api.post('/prediction')
def ml_prediction(kl_infos:  Kline):
    """
    prediction for the next hour close value for cryptocurrency
        
    """
    print('debut de la prediction')
    
    kline_param = [{
    'open' : kl_infos.Open,
    'high' : kl_infos.High,
    'low' : kl_infos.Low,
    'close' : kl_infos.Close,
    'volume' : kl_infos.Volume,
    'trades' : kl_infos.Trades
    }]
    # store kline param type by the user in a dataframe 
    kline_df = pd.DataFrame(kline_param, columns = [ 'open', 'high', 'low', 'close', 'volume', 'trades'])
    
    # les features sont : 'open', 'high', 'low', 'close', 'volume', 'trades'
    
    #kline_df = kline_df.iloc[0:, 2:8]
    print('contenu du kline_df :',kline_df.values )
    # Chargement du scaler
    scaler = joblib.load("scaler.pkl")
    # Appliquer le scaler
    print(' debut du scaled ======================')
    kline_scaled = scaler.transform(kline_df)
    print ('donnees apres le scaled : ', kline_scaled )
    # chargement du modele de prediction a appliquer
    # regression
    print(' debut de la regression')
    model_regressor = joblib.load('gb_regressor_model.pkl')
    prediction_reg = model_regressor.predict(kline_scaled) #.values)
    print('fin de la regression, resultat : ', prediction_reg)

    #classification
    model_classifier = joblib.load('gb_classifier_model.pkl')
    prediction_class = model_regressor.predict(kline_scaled) #.values)
    print(' la prediction class ==========', prediction_class)

    
    return {
        'regression: result of next hour close value ': prediction_reg[0],
        'classification: result of next hour close value ': prediction_class[0]
    }