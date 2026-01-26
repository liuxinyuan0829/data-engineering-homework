#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
import click

@click.command()
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default=5433, type=int, help='PostgreSQL port')
@click.option('--db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--table', default='yellow_taxi_data', help='Target table name')
@click.option('--year', default=2025, help='year of the data')
@click.option('--month', default=11, help='month of the data')

def run(user, password, host, port, db, table, year, month):
    # create db engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # dwonload green trip data
    df = pd.read_parquet(f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{year}-{month:02d}.parquet')

    # create schema and insert data

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        )
    df.head(0).to_sql(name=table,con=engine, if_exists='replace')
    df.to_sql(name=table,con=engine, if_exists='append')

    # dwonload taxi zone data
    df_zone = pd.read_csv('https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv')

    # create schema and insert data

    df_zone.columns = (
        df_zone.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        )
    df_zone.head(0).to_sql(name='taxi_zone_lookup',con=engine, if_exists='replace')
    df_zone.to_sql(name='taxi_zone_lookup',con=engine, if_exists='append')

if __name__ =='__main__':
    run()