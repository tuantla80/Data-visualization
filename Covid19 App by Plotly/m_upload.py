import pandas as pd
from datetime import datetime
from pprint import pprint
from dotenv import load_dotenv
import os

from mdb import MongoDB


if __name__ == '__main__':
    print(f'Upload data to MongoDB: Start at {datetime.now()}')
    dotenv_file_path = r'.env'
    load_dotenv(dotenv_file_path)
    host = os.environ.get('MONGODB_HOST')
    port = int(os.environ.get('MONGODB_PORT'))
    db_name = os.environ.get('MONGODB_DB_NAME')

    # Upload confirmed
    mdb_confirmed = MongoDB(host, port, db_name, collection_name=os.environ.get('MONGODB_COLLECTION_confirmed'))
    df_confirmed = pd.read_csv('time_series_covid19_confirmed_global.csv')
    mdb_confirmed.upload_df(df=df_confirmed)

    # Upload deaths
    mdb_deaths = MongoDB(host, port, db_name, collection_name=os.environ.get('MONGODB_COLLECTION_deaths'))
    df_deaths = pd.read_csv('time_series_covid19_deaths_global.csv')
    mdb_deaths.upload_df(df=df_deaths)

    # Upload recovered
    mdb_recovered = MongoDB(host, port, db_name, collection_name=os.environ.get('MONGODB_COLLECTION_recovered'))
    df_recovered = pd.read_csv('time_series_covid19_recovered_global.csv')
    mdb_recovered.upload_df(df=df_recovered)

    # print(df_confirmed[0:2].to_string())
    print('df_confirmed.shape = ', df_confirmed.shape)
    print('df_deaths.shape = ', df_deaths.shape)
    print('df_recovered.shape = ', df_recovered.shape)