Le dossier API contient en local un dossier 'models' avec toutes les modèles entrainés et les scalers pour les prédictions des prix des cryptos.
Pour lancer un container à partir de l'image opa-api, il est nécessaire de créer un fichier '.env' avec:

DB_USER
DB_PASSWORD
DB_ADRESS
qui sera utilisé lors de lancement:docker run --env-file .venv -p 8000:8000 sokhnamery/opa-api
