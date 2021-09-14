import requests
import json
import pandas as pd
from apscheduler.schedulers.blocking import BlockingScheduler
import apscheduler.schedulers.blocking
from datetime import datetime,timedelta
import time
import sqlalchemy
import sys
import numpy as np

# taxa de periodicidade para realizar a operação
periodicidade = 1

# indica se a aplicação está rodando dentro ou fora do docker True = docker False = Fora do docker 
interno = False

# Se verdadeiro, deleta os dados da tabela temporaria apos trata-los 
deleteAfterInsert = False

# Engine de conexão com banco de dados
database_connection = 'mysql+mysqldb://{user}:{password}@{server}:{port}/{database}'

def perMinuteTicker():
    dtfechamento = datetime.utcnow() - timedelta(seconds=1)
    print(dtfechamento)
    dtabertura = dtfechamento - timedelta(minutes=periodicidade)
    print(dtabertura)
    
    querySelect = "SELECT *  \
            FROM TEMP WHERE DATETIME BETWEEN '%Y-%m-%d %H:%M:%S' AND '#Y-#m-#d #H:#M:#S'" 
    
    querySelect = dtabertura.strftime(querySelect)
    querySelect = querySelect.replace('#','%')
    querySelect = dtfechamento.strftime(querySelect)
    print(querySelect)
    
    dataframe = pd.read_sql(querySelect,con=database_connection)
    dataframe['DATETIME']= pd.to_datetime(dataframe['DATETIME'])

    abertura = dataframe[(dataframe['DATETIME'] == dtabertura.strftime('%Y-%m-%d %H:%M:%S'))]
    abertura = abertura[['CRIPTOMOEDA', 'PRECO']]
    abertura.rename(columns={'PRECO': 'ABERTURA'}, inplace=True)

    fechamento = dataframe[(dataframe['DATETIME'] == (dtfechamento - timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S'))]
    fechamento = fechamento[['CRIPTOMOEDA', 'PRECO']]
    fechamento.rename(columns={'PRECO': 'FECHAMENTO'}, inplace=True)

    high = dataframe[['CRIPTOMOEDA', 'PRECO']]
    high = high.groupby("CRIPTOMOEDA").max()
    high.rename(columns={'PRECO': 'MAXIMO'}, inplace=True)

    low = dataframe[['CRIPTOMOEDA', 'PRECO']]
    low = low.groupby("CRIPTOMOEDA").min()
    low.rename(columns={'PRECO': 'MINIMO'}, inplace=True)
    
    ticker = pd.merge(pd.merge(pd.merge(abertura,fechamento,on='CRIPTOMOEDA'),high,on='CRIPTOMOEDA'),low,on='CRIPTOMOEDA')
    ticker['DATETIME'] = dtfechamento.strftime('%Y-%m-%d %H:%M:%S')
    ticker['PERIODICIDADE'] = periodicidade
    ticker = ticker.reset_index()
    ticker = ticker[['CRIPTOMOEDA', 'ABERTURA','FECHAMENTO','MAXIMO','MINIMO','DATETIME','PERIODICIDADE']]
    ticker.to_sql('CANDYSTICKS',con=database_connection,if_exists='append', index=False)

    if deleteAfterInsert:
        print('deletando')
        queryDelete = "DELETE \
            FROM TEMP WHERE DATETIME < '%Y-%m-%d %H:%M:%S'" 
        queryDelete = dtabertura.strftime(queryDelete)
        queryDelete = (dtfechamento - timedelta(minutes=15)).strftime(queryDelete)
        connection = database_connection.connect()
        connection.execute(sqlalchemy.text(queryDelete))


if __name__ == "__main__":
    args = sys.argv
    print(sys.argv)
    periodicidade = int(args[1]) #Argumento de periodicidade
    interno = bool((args[2]=='True' and 1 or 0)) #Argumento fora ou no docker
    deleteAfterInsert = bool((args[3]=='True' and 1 or 0)) #Argumento se deleta dados analisados
    
    databaseParams = json.load(open('databaseParams.json'))
    print(databaseParams)
    database_connection = database_connection.format(user=databaseParams['user'],
                  password=databaseParams['password'],
                  server=databaseParams[(interno and 'serverInternal' or 'serverExternal')],
                  port=databaseParams[(interno and 'portInternal' or 'portExternal')],
                  database=databaseParams['database'])
    database_connection = sqlalchemy.create_engine(database_connection)
    minuteString = str(np.arange(0, 59, periodicidade)).replace(" ",",").replace(",,",",")[2:-1]

    scheduler = BlockingScheduler()
    scheduler.add_job(perMinuteTicker, 'cron', minute=minuteString,second='1',max_instances=10)
    scheduler.start()
