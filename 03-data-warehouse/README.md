Question 1. Counting records
What is count of records for the 2024 Yellow Taxi Data?

ANSWER: 20,332,093

```SQL
-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `theta-carving-486822-c0.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['gs://de-data-warehouse-bucket/yellow_tripdata_2024-*.parquet']
);

-- Get records count
select count(VendorID) from theta-carving-486822-c0.nytaxi.external_yellow_tripdata;
```

Question 2. Data read estimation
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

ANSWER: 0 MB for the External Table and 155.12 MB for the Materialized Table


```SQL
-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE theta-carving-486822-c0.nytaxi.yellow_tripdata_non_partitioned AS
SELECT * FROM theta-carving-486822-c0.nytaxi.external_yellow_tripdata;

-- Get unique PULocationID count from external table
select count(distinct PULocationID) from theta-carving-486822-c0.nytaxi.external_yellow_tripdata;

-- Get unique PULocationID count from materialized table
select count(distinct PULocationID) from theta-carving-486822-c0.nytaxi.yellow_tripdata_non_partitioned;
```

Question 3. Understanding columnar storage
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table.
Why are the estimated number of Bytes different?

ANSWER: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.


Question 4. Counting zero fare trips
How many records have a fare_amount of 0?

ANSWER: 8,333

```SQL
select count(VendorID) from theta-carving-486822-c0.nytaxi.yellow_tripdata_non_partitioned 
where fare_amount = 0;
```

Question 5. Partitioning and clustering
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

ANSWER: Partition by tpep_dropoff_datetime and Cluster on VendorID

```SQL
-- Creating a partition and cluster table
CREATE OR REPLACE TABLE theta-carving-486822-c0.nytaxi.yellow_tripdata_partitioned_clustered
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY VendorID AS
SELECT * FROM theta-carving-486822-c0.nytaxi.external_yellow_tripdata;
```

Question 6. Partition benefits
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

ANSWER: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table

```SQL
-- get VendorID count in non_partitioned table
SELECT count(VendorID) as VendorID_count
FROM theta-carving-486822-c0.nytaxi.yellow_tripdata_non_partitioned
WHERE DATE(tpep_pickup_datetime) BETWEEN '2024-03-01' AND '2024-03-15'

-- get VendorID count in partitioned table
SELECT count(VendorID) as VendorID_count
FROM theta-carving-486822-c0.nytaxi.yellow_tripdata_partitioned_clustered
WHERE DATE(tpep_pickup_datetime) BETWEEN '2024-03-01' AND '2024-03-15'
```

Question 7. External table storage
Where is the data stored in the External Table you created?

ANSWER: GCP Bucket

Question 8. Clustering best practices
It is best practice in Big Query to always cluster your data:

ANSWER: False

Question 9. Understanding table scans
No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

ANSWER: Because BigQuery can answer SELECT COUNT(*) from a materialized/optimized table using metadata, without scanning any table blocks — so the bytes processed shows as 0 B.