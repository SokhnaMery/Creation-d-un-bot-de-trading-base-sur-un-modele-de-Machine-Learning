import os
import psycopg2

# Récupération des variables d'environnement
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
address = os.getenv("DB_ADDRESS")

print(f"DB_USER: {user}")
print(f"DB_PASSWORD: {password}")
print(f"DB_ADDRESS: {address}")

# Vérifiez si les variables d'environnement sont définies
if not user or not password or not address:
    raise ValueError("One or more required environment variables are not set")

# Connexion à la base de données
conn_string = f"postgresql://{user}:{password}@{address}:5432/database_binance"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

print("Connection successful!")
