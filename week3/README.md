# Week 3 Overview

[3.1.1 - Data Warehouse and BigQuery](#311---data-warehouse-and-bigquery)<br />
[3.1.2 - Partitioning and Clustering](#312---partitioning-and-clustering)<br />


## [3.1.1 - Data Warehouse and BigQuery](https://www.youtube.com/watch?v=jrHljAoD6nM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=25)
**1. OLAP vs. OLTP**<br />
**On-Line Transaction Processing (OLTP)** systems are typically used in backend services, where sequences of SQL statements are grouped together in the form of transactions, which are rolled back if any of their statements fails. These systems deal with fast and small updates, store data in normalized databases that reduce data redundancy and increase productivity of end users.<br />

**On-Line Analytical Processing (OLAP)** systems are composed by denormalized databases, which simplify analytics queries, and are mainly used for data mining.
Data Warehouses are the main example in this category. They generally contain data from many sources (e.g., different OLTP systems) and implement star or snowflake schemas that are optimized for analytical tasks.<br />

**2. BigQuery**<br />
**BigQuery** is a Data Warehouse solution from Google. Its main advantages are: <br />
* no servers to manage or software to install; <br />
* software & infrastructure: high scalability and availability; <br />
* builtin features like machine learning, geospatial analysis and business inteligence directly from the SQL interface.
* separate the compute engineer and data storage

**3. BigQuery Interface**<br />
BigQuery provides a lot of open source data. For example, we can search for the citibike_stations public data in BigQuery.
![bigquery_interface.png](./img/bigquery_interface.png)<br />
And then you can do some queries, and even save the results or explore data more with google colob .etc.
```
SELECT station_id, name FROM `bigquery-public-data.new_york_citibike.citibike_stations` LIMIT 100;
```

**4. Create External tabels**<br />
According to [BigQuery's documentation](https://cloud.google.com/bigquery/docs/external-data-sources):<br />
**External tables** are similar to standard BigQuery tables, in that these tables store their metadata and schema in BigQuery storage. However, their data resides in an external source.<br />
External tables are contained inside a dataset, and you manage them in the same way that you manage a standard BigQuery table.<br />
Here, we create an external table for our yellow taxi trips data. <br />
First, we need to upload 7 parquet files of 2021 available at the [data source](https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/yellow). Here I used prefect cloud without previous deploments on week 2, so I first create a deployment again and then run with available month 1-7.
```
conda activate de
prefect cloud login -k your-api-key-here
cd ../week2/
python docker_deploy.py
prefect agent start -q default
prefect deployment run etl-parent-flow/docker-flow -p "months=[1, 2, 3, 4, 5, 6, 7]"
```
Then we crate an external table called external_yellow_tripdata_2021. Please note that dtc-de-373006 is the id of my project, and trips_data_all is the name of my dataset, and you can replace with yours.
```
CREATE OR REPLACE EXTERNAL TABLE `dtc-de-373006.trips_data_all.external_yellow_tripdata_2021`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dtc_data_lake_dtc-de-373006/data/yellow/yellow_tripdata_2021-*.parquet']
);

SELECT * FROM `dtc-de-373006.trips_data_all.external_yellow_tripdata_2021` limit 10;
```
![external_table.png](./img/external_table.png)<br />


**5. Partitioning in Big Query**<br />
When we create a dataset, we generally have one or more columns that are used as some type of filter. In this case, we can partition a table based on such columns to improve BigQuery's performance. In this lesson, the instructor shows us an example of a dataset containing StackOverflow questions (left), and how the dataset would look like if it was partitioned by the Creation_date field (right).<br />
![partition.png](./img/partition.png)<br />
Partitioning is a powerful feature of BigQuery. Suppose we want to query the questions created on a specific date. Partition improves processing, because BigQuery will not read or process any data from other dates. This improves efficiency and reduces querying costs.<br />

To illustrate the difference in performance, we first create a non partitioned data table from our dataset.
```
CREATE OR REPLACE TABLE `dtc-de-373006.trips_data_all.yellow_tripdata_non_partitioned` AS
SELECT * FROM `dtc-de-373006.trips_data_all.external_yellow_tripdata_2021`;
```
Then we create a partitioned table.
```
CREATE OR REPLACE TABLE `dtc-de-373006.trips_data_all.yellow_tripdata_partitioned` 
PARTITION BY DATE(tpep_pickup_datetime) AS
SELECT * FROM `dtc-de-373006.trips_data_all.external_yellow_tripdata_2021`;
```
You can see the difference in the icons between regular and partitioned tables. From the details, you can also tell which column the table was partitioned by.<br />
![partition_table1.png](./img/partition_table1.png)<br />

Now, let's compare the difference in performance when querying non partitioned and partitioned data.
```
SELECT DISTINCT(PULocationID)
FROM `dtc-de-373006.trips_data_all.yellow_tripdata_non_partitioned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2021-01-01' AND '2021-06-30';

SELECT DISTINCT(PULocationID)
FROM `dtc-de-373006.trips_data_all.yellow_tripdata_partitioned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2021-01-01' AND '2021-06-30';
```
![partition_table2.png](./img/partition_table2.png)<br />
Here we can see the large difference in processing and billing (in this example, more than 10x improvement when using partitioned data).
And if look into partitions.
```
SELECT table_name, partition_id, total_rows
FROM trips_data_all.INFORMATION_SCHEMA.PARTITIONS
WHERE table_name = 'yellow_tripdata_partitioned'
ORDER BY total_rows DESC;
````
![partition_table3.png](./img/partition_table3.png)<br />


**6. Clustering in Big Query**<br />
We can cluster tables based on some field. In the StackOverflow example presented by the instructor, after partitioning questions by date, we may want to cluster them by tag in each partition. Clustering also helps us to reduce our costs and improve query performance. The field that we choose for clustering depends on how the data will be queried.<br />
![cluster_table1.png](./img/cluster_table1.png)<br />

Creating a clustered data for our dataset.
```
CREATE OR REPLACE TABLE `dtc-de-373006.trips_data_all.yellow_tripdata_partitioned_clustered`
PARTITION BY DATE(tpep_pickup_datetime)
CLUSTER BY PULocationID AS
SELECT * FROM `dtc-de-373006.trips_data_all.external_yellow_tripdata_2021`;
```
Now, let's compare the difference in performance when querying unclustered and clustered data.
```
SELECT count(*) as trips
FROM `dtc-de-373006.trips_data_all.yellow_tripdata_partitioned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2021-01-01' and '2021-10-31'
AND PULocationID = 132;

SELECT count(*) as trips
FROM `dtc-de-373006.trips_data_all.yellow_tripdata_partitioned_clustered`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2021-01-01' and '2021-10-31'
AND PULocationID = 132;
```
![cluster_table2.png](./img/cluster_table2.png)<br />


## [3.1.2 - Partitioning and Clustering](https://www.youtube.com/watch?v=-CqXf7vhhDs&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=26)
**1. BigQuery Partition**<br />
we can partition data by a time-unit column, ingestion time (_PARTITIONTIME) or an integer range partitioning. <br />
When partitioning data, to achieve its full potential, we would prefer evenly distributed partitions. In addition, we must take into account the number of partitions that we will need. <br />
When using Time unit or ingestion time, we do it Daily by Default, but you can also use Hourly, Monthly or yearly based on how large you data is. <br />BigQuery limits the number of partitions to 4000.

**2. BigQuery Clustering**<br />
When clustering, a maximum of four columns can be used and the order that are specified is important to determine how the data will be sorted. <br />Clustering improves filtering and aggregation queries, but typically doesn't show much improvement for tables with less than 1 GB of data.<br />

**3. Partitioning vs Clustering**<br />
![comparison.png](./img/comparison.png)<br />
It is usually better to using Clustering when: 
* partitioning creates small partitions (e.g., each partition < 1 GB)
* partitionining generates more than 4000 partitions
* we need to update/modify data in the majority of partitions on a frequent basis.

