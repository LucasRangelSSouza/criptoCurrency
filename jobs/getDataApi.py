import requests
import json
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
import apscheduler.schedulers.blocking
from datetime import datetime
import time
import sqlalchemy

def getApiData():
    dt = datetime.utcnow()
    url='https://poloniex.com/public?command=returnTicker';
    response = requests.get(url, verify=False)
    ticker = pd.DataFrame(response.json())
    moedas = list(ticker.columns.values)
    ticker = ticker.T
    ticker['CRIPTOMOEDA'] = moedas
    ticker.reset_index(drop=True, inplace=True)
    collumsToDrop = ["id","percentChange", "baseVolume", "quoteVolume", "isFrozen", "postOnly", "high24hr", "low24hr",'lowestAsk','highestBid']
    ticker.drop(collumsToDrop, axis=1, inplace=True)
    ticker.rename(columns={'last': 'PRECO'}, inplace=True)
    ticker['DATETIME'] = dt.strftime('%Y-%m-%d %H:%M:%S')
    database_connection = sqlalchemy.create_engine('mysql+mysqldb://{user}:{password}@{server}:{port}/{database}'
                                                   .format(user='admin', password='789123', server='mysql', port='3306',  database='currency'))
    ticker.to_sql(name='TEMP',con=database_connection,if_exists='append', index=False)
scheduler = BlockingScheduler()
scheduler.add_job(getApiData, 'cron', second='*',max_instances=10)
scheduler.start()






