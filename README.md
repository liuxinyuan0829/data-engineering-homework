# data-engineering-homework
data-engineering-homework-codespace

Question 1: 25.3
    command:
    docker run -it --rm --entrypoint=bash python:3.13
    pip -V

Question 2: postgres:5432 and db:5432

Prepare the data:
    command:
    pip install uv
    uv init --python=3.13
    uv add pandas pyarrow
    add to .gitnore: *.parquet
    uv add sqlalchemy psycopg2-binary
    
    run the python script to insert data into postgres:
    uv run python ingest_data.py \
    --user=postgres \
    --password=postgres \
    --host=localhost \
    --port=5433 \
    --db=ny_taxi \
    --table=green_trip_data \
    --year=2025 \
    --month=11

Question 3: 8007
SQL:
select count(*) from public.green_trip_data 
where lpep_pickup_datetime >= '2025-11-01' and lpep_pickup_datetime < '2025-12-01'
and trip_distance <= 1;

Question 4: 2025-11-20
SQL:
select 
cast(lpep_pickup_datetime as date) as pickup_date
, sum(trip_distance) as total_trip_distance
from public.green_trip_data
where trip_distance <= 100
group by cast(lpep_pickup_datetime as date)
order by sum(trip_distance) desc
limit 1
;


Question 5: East Harlem North
SQL:
select 
t.Zone
, sum(g.trip_distance) as total_trip_distance
from public.green_trip_data as g
join public.taxi_zone_lookup as t on g.PULocationID  = t.LocationID
where g.trip_distance <= 100
and g.lpep_pickup_datetime >= '2025-11-18' and g.lpep_pickup_datetime < '2025-11-19'
group by t.Zone
order by sum(trip_distance) desc
limit 1
;


Question 6: Yorkville West
SQL:
select 
p.Zone as pick_up_zone
, d.Zone as drop_down_zone
, g.tip_amount
from public.green_trip_data as g
join public.taxi_zone_lookup as p on g.puLocationID  = p.LocationID
join public.taxi_zone_lookup as d on g.dolocationID  = d.LocationID
where g.lpep_pickup_datetime >= '2025-11-01' and g.lpep_pickup_datetime < '2025-12-01'
and p.Zone = 'East Harlem North'
order by g.tip_amount desc
limit 1
;