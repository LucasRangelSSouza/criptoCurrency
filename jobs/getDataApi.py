import requests
import json
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
import apscheduler.schedulers.blocking
from datetime import datetime
import time
import sqlalchemy
import sys

# Engine de conexão com banco de dados
database_connection = 'mysql+mysqldb://{user}:{password}@{server}:{port}/{database}'

def getApiData():
    
    #obtem data utc
    dt = datetime.utcnow()
    
    #Chama API
    url='https://poloniex.com/public?command=returnTicker';
    response = requests.get(url, verify=False)
    
    # transforma os dados recebidos em um DataFrame Pandas
    ticker = pd.DataFrame(response.json())
    
    #Homogeniza e trata os dados
    moedas = list(ticker.columns.values)
    ticker = ticker.T
    ticker['CRIPTOMOEDA'] = moedas
    ticker.reset_index(drop=True, inplace=True)
    collumsToDrop = ["id","percentChange", "baseVolume", "quoteVolume", "isFrozen", "postOnly", "high24hr", "low24hr",'lowestAsk','highestBid']
    ticker.drop(collumsToDrop, axis=1, inplace=True)
    ticker.rename(columns={'last': 'PRECO'}, inplace=True)
    ticker['DATETIME'] = dt.strftime('%Y-%m-%d %H:%M:%S')

    #Salva os dados na tabela TEM do banco de dados
    ticker.to_sql(name='TEMP',con=database_connection,if_exists='append', index=False)

if __name__ == "__main__":
    args = sys.argv
    interno = bool((args[1]=='True' and 1 or 0)) #Argumento fora ou no docker
    databaseParams = json.load(open('databaseParams.json'))
    database_connection = database_connection.format(user=databaseParams['user'],
                  password=databaseParams['password'],
                  server=databaseParams[(interno and 'serverInternal' or 'serverExternal')],
                  port=databaseParams[(interno and 'portInternal' or 'portExternal')],
                  database=databaseParams['database'])
    database_connection = sqlalchemy.create_engine(database_connection)

    scheduler = BlockingScheduler()
    scheduler.add_job(getApiData, 'cron', second='*',max_instances=10)
    scheduler.start()






