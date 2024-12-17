import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import pyarrow.parquet as parquet
import os


def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name_green = params.table_name_green
    table_name_zones = params.table_name_zones
    url_green = params.url_green
    url_zone = params.url_zone

    # variable for generated filenames
    parquet_file = 'green_taxi.parquet'
    csv_file_green = 'green_trip_data_2019-09.csv'
    csv_file_zone = 'taxi_zone_lookup.csv'

    # download the csv file
    os.system(f"curl -o {parquet_file} {url_green}")
    os.system(f"curl -o {csv_file_zone} {url_zone}")

    # conversion of green taxi parquet to green taxi csv
    table = parquet.read_table(parquet_file)
    df_parquet = table.to_pandas()
    df_parquet.to_csv(csv_file_green, index=False)


# Create engine for your created postgres
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

# Initialize zones data and upload it to DB
    # read the csv using pandas
    df_zones = pd.read_csv(csv_file_zone)
    # get the columns names and add it with replace setting first
    df_zones.head(n=0).to_sql(name=table_name_zones, con=engine, if_exists='replace')
    # upload the actual data
    df_zones.to_sql(name=table_name_zones, con=engine, if_exists='append')

    print('Done for zones upload')

# Initialize green trips data and upload it to DB
    # read the csv using pandas with iteration due to its large record of data
    df_iter_green = pd.read_csv(csv_file_green, iterator=True, chunksize=100000)
    # initialize the first iteration
    df_green = next(df_iter_green)
    # modify some columns to a much proper data type
    df_green.lpep_dropoff_datetime = pd.to_datetime(df_green.lpep_dropoff_datetime)
    df_green.lpep_pickup_datetime = pd.to_datetime(df_green.lpep_pickup_datetime)
    # get the columns names and add it with replace setting first
    df_green.head(n=0).to_sql(name=table_name_green, con=engine, if_exists='replace')
    # upload the actual data first batch
    df_green.to_sql(name=table_name_green, con=engine, if_exists='append')
    # loop through the remaining iterations/batch using enumerate function
    for batch, df_green in enumerate(df_iter_green):
        df_green.lpep_pickup_datetime = pd.to_datetime(df_green.lpep_pickup_datetime)
        df_green.lpep_dropoff_datetime = pd.to_datetime(df_green.lpep_dropoff_datetime)
        # record time for each batch upload
        t_start = time()
        df_green.to_sql(name=table_name_green, con=engine, if_exists='append')
        t_end = time()
        print(f'inserted chunk {batch}..., took %.3f second' % (t_end - t_start))

    print('Done!')


# check if the script is being run directly
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # user
    # password
    # host
    # port
    # database name
    # table name green
    # table name zones
    # url of the green taxi parquet
    # url of the nyc zone lookup table csv

    parser.add_argument('--user', help='user for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database for postgres')
    parser.add_argument('--table-name-green', help='table-name of green texi trips for postgres')
    parser.add_argument('--table-name-zones', help='table-name of zones for postgres')
    parser.add_argument('--url-green', help='url for green taxi parquet link')
    parser.add_argument('--url-zone', help='url for nyc taxi zone lookup table csv link')

    args = parser.parse_args()

    main(args)

""" 
This can be improved as it is not recommended to pass the password value directly, it must be through environmental 
variables or other means

    
docker build -t taxi_ingest:v1 .
    
URL_GREEN="https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-09.parquet"
URL_ZONE="https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
docker run -it \
--network=pg-network \
taxi_ingest:v1 \
    --user=root \
    --password=root \
    --host=dataingestiontopostgrescoderepo-pgdatabase-1 \
    --port=5432 \
    --db=ny_taxi \
    --table-name-green=green_taxi_trips \
    --table-name-zones=zones \
    --url-green=${URL_GREEN} \
    --url-zone=${URL_ZONE}
    
    

"""


