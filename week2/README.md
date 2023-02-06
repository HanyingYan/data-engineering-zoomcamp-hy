# Week 2 Overview

[2.1.1 - Data Lake](#211---data-lake)<br />
[2.2.1 - Introduction to Workflow](#221---introduction-to-workflow)<br />
[2.2.2 - Introduction to Prefect Concepts](#222---introduction-to-prefect-concepts)<br />
[2.2.3 - ETL with GCP & Prefect](#223---etl-with-gcp--prefect)<br />
[2.2.4 - From Google Cloud Storage to Big Query](#224---from-google-cloud-storage-to-big-query)<br />
[2.2.5 - Parametrizing Flow & Deployments with ETL into GCS flow](#225---parametrizing-flow--deployments-with-etl-into-gcs-flow)<br />
[2.2.6 - Schedules & Docker Storage with Infrastructure](#226---schedules--docker-storage-with-infrastructure)<br />
[2.2.7 - Prefect Cloud/Additional resources](#227---prefect-cloudadditional-resources)

## [2.1.1 - Data Lake](https://www.youtube.com/watch?v=W3Zm6rjOq70&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=17)
**1. What is a Data Lake?**
* Data Lake is a central repository that holds big data from many sources, structured, semi-structured or even unstructured. The idea is to ingest data as quickly as possible and make it available or accessible to other team members like DS, DA, DE.etc<br />
* Generally in your data lake you would associate some sort of metadata for faster access.<br />
* A data lake solution generally need to be secure and can scale. Also, the hardware should be inexpensive because you want to store as much of data as quickly as possible..<br />

**2. Data Lake vs Data Warehouse**<br />
A Data Lake stores a huge amount of data and are normally used for stream processing, machine learning and real time analytics. <br />
On the other hand, a Data Warehouse stores structured data for analytics and batch processing.

**3. How did it start?**
* Companies realized the value of data
* Store and access data quickly
* Cannot always define structure of data
* Usefulness of data being realized later in the project lifecycle
* Increase in data scientists
* R&D on data products
* Need for Cheap storage of Big data

**4. Extract Transform Load (ELT) vs. Extract Load and Transform (ETL)**
* [ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) is mainly used for a small amount of data whereas ELT is used for large amounts of data
* ELT provides data lake support (Schema on read) where ETL is data warehouse solution (Schema on write)

**5. Gotcha of Data Lake**
* Converting into Data Swamp
* No versioning
* Incompatible schemas for same data without versioning
* No metadata associated
* Joins not possible
		
**6. Cloud provider for data lake**
* GCP - cloud storage
* AWS - S3
* AZURE - AZURE BLOB


## [2.2.1 - Introduction to Workflow](https://www.youtube.com/watch?v=8oLs6pzHp68&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=18)
**1. Data Flow and Data Flow Diagram**<br />
[Data flow](https://en.wikipedia.org/wiki/Dataflow) is the transfer of data from a source to a destination.  If we get more technical, an ETL (extract, transform, load) process is a type of data flow.<br />
A [data flow diagram (DFD)](https://en.wikipedia.org/wiki/Data-flow_diagram) is a way of representing a flow of data through a process or a system (usually an information system). And it is a Directed Acyclic Graph (DAG) with arrows to indicate direction, and acyclic so no cycle with clear dependency.

**2. Workflow and Workflow Orchestration**<br />
A [workflow](https://en.wikipedia.org/wiki/Workflow) consists of an orchestrated and repeatable pattern of activity, enabled by the systematic organization of resources into processes that transform materials, provide services, or process information. <br />
Workflow orchestration is the automation of a workflow or multiple tasks. In other words, it handles multiple automated tasks to execute a single significant process or workflow.<br />
Workflow engines as tools let us define the DAG and parametrize the graph, they also have return mechanism with history/logs.
* Prefect
* Make
* Luigi
* Apache Airflow


## [2.2.2 - Introduction to Prefect Concepts](https://www.youtube.com/watch?v=cdtN6dhp708&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=19)
**Step 1**<br />
start PostgreSQL and PgAdmin4 using docker-compose with [*docker-compose.yml*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/docker-compose.yml)
```
cd ~/data-engineering-zoomcamp-hy/week2
docker compose down
docker compose up -d
```
Then set up a conda environment with required packages from [*requirements.txt*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/requirements.txt) and then ingest our Yellow Taxi Data with [*ingest_data.py*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/ingest_data.py)
```
code .
conda create -n de pythonb=3.9
conda env list
conda activate de
pip install -r requirements.txt
python ingest_data.py
```
Now we have access to the database by logging in PgAdmin4 at [http://localhost:8080/](http://localhost:8080/) with credentials or using pgcli
```
pgcli -h localhost -p 5432 -user root -d ny_taxi
```
However, it would be better to run the script on schedule instead of manually trigger it by using some workflow orchestration tools.

**Step 2**<br />
We can use ```@flow``` decorator to indicate a Prefect flow, and ```@task``` decorator to indicate a Prefect task. By breaking our codes into three tasks - extract_data(E), transform_data(T), ingest_data(L), we get [*ingest_data_flow.py*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/ingest_data_flow.py)  
after running 
```
python ingest_data_flow.py
```
you can get an output like below with 3 task extract_data-976b417c-0, transform_data-7a5e1946-0 and ingest_data-e7246262-0:
```
21:15:08.819 | INFO    | prefect.engine - Created flow run 'grinning-lemur' for flow 'Ingest flow'
21:15:09.052 | INFO    | Flow run 'grinning-lemur' - Created subflow run 'awesome-capuchin' for flow 'Subflow'
21:15:09.107 | INFO    | Flow run 'awesome-capuchin' - Logging Subflow for: yellow_taxi_trips
21:15:09.152 | INFO    | Flow run 'awesome-capuchin' - Finished in state Completed()
21:15:09.192 | INFO    | Flow run 'grinning-lemur' - Created task run 'extract_data-976b417c-0' for task 'extract_data'
21:15:09.193 | INFO    | Flow run 'grinning-lemur' - Executing 'extract_data-976b417c-0' immediately...
21:15:09.244 | INFO    | Task run 'extract_data-976b417c-0' - Finished in state Cached(type=COMPLETED)
21:15:09.449 | INFO    | Flow run 'grinning-lemur' - Created task run 'transform_data-7a5e1946-0' for task 'transform_data'
21:15:09.450 | INFO    | Flow run 'grinning-lemur' - Executing 'transform_data-7a5e1946-0' immediately...
21:15:09.507 | INFO    | Task run 'transform_data-7a5e1946-0' - pre:missing passenger count: 1973
21:15:09.526 | INFO    | Task run 'transform_data-7a5e1946-0' - post:missing passenger count: 0
21:15:09.555 | INFO    | Task run 'transform_data-7a5e1946-0' - Finished in state Completed()
21:15:09.587 | INFO    | Flow run 'grinning-lemur' - Created task run 'ingest_data-e7246262-0' for task 'ingest_data'
21:15:09.588 | INFO    | Flow run 'grinning-lemur' - Executing 'ingest_data-e7246262-0' immediately...
21:15:25.848 | INFO    | Task run 'ingest_data-e7246262-0' - Finished in state Completed()
21:15:25.875 | INFO    | Flow run 'grinning-lemur' - Finished in state Completed('All states completed.')
```

**Step 3**<br />
Run Prefect Orion UI
```
prefect orion start
#don't forget to set config if it's your first time running it
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```
Prefect Orion UI allows us to see our flows in an interactive an intuitive web interface. It summarizes the state of our workflows. Besides, we also have some extra information, such as:
* Task Run Concurrency, which can be configured by adding tags to tasks.
* Notifications, that alerts us when something goes wrong.
* Blocks, which allows us to store configurations and use them as an interface for interacting with external systems. In other words, we can securely store authentication credentials for different services, without the need to specify such credentials directly in our codes or command lines.

**Step 4**<br />
Create a new block for our PostgreSQL connector. In Prefect Orion UI:
* click in "Blocks" and then "Add Block +". 
* add a SQLAlchemyConnector, and fill the corresponding form with crendentials. Mine is 
```{ "driver": "postgresql+psycopg2", "database": "ny_taxi", "username": "root", "password": "root", "host": "localhost", "port": "5432" }```
* click on "Create" and you will be able to use the following snippet in your script to run without crendentials.(line 44-45 of [*ingest_data_flow.py*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/ingest_data_flow.py))
```
from prefect_sqlalchemy import SqlAlchemyConnector
with SqlAlchemyConnector.load("postgres-connector") as database_block:
    ...
```


## [2.2.3 - ETL with GCP & Prefect](https://www.youtube.com/watch?v=W-rMz_2GwqQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=20)
**Step 1**<br />
Write ETL script [*etl_web_to_gcs.py*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/etl_web_to_gcs.py) to save data downloaded from [archive place](https://github.com/DataTalksClub/nyc-tlc-data) locally to [data/yellow]().
We divided the flow into 3 different task - fetch(E), clean(T) and write_local(L).<br />
You can run Prefect Orion UI from terminal
```
prefect orion start
```
Please note that when you try to download data from a web, we can add the retries to our task function in case it doesn't work for some reasons. (line 8&11-12 of [*etl_web_to_gcs.py*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/etl_web_to_gcs.py)

**Step 2**<br />
Prefect Orion UI -> Blocks -> create new GCS Bucket Block to store our GCP credentials.<br />
Please note you can first register it if GCS Bucket Block is not available by
```
prefect block register -m prefect_gcp
```
You can assign *gcp-zoomcamp* to Block Name, and the name of the bucket is unique, which you should already generated from week 1 with a name similar to *dtc_data_lake_dtc-de-373006*. <br />
Then you may also need to create a GCP credential block if you don't have one. Mine is with name *gcp-zoomcamp-credentials*. And for the service account info, you can either inform the path of your json file (*/Users/hanying/Documents/data-engineering-zoomcamp-hy/dtc-de-373006-58eecc9ef188.json*), or paste the contents directly in the blue box under "The contents of the keyfile as dict".  <br />
Please make sure you don't upload your credential .json files to github (by adding to your *.gitignore*) or other public space. <br />
Now you can use this block as sugegsted with 
```
from prefect_gcp.cloud_storage import GcsBucket
gcp_cloud_storage_bucket_block = GcsBucket.load("gcp-zoomcamp")
```

**Step 3**<br />
Create a new task - write_gcs() and run [*etl_web_to_gcs.py*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/etl_web_to_gcs.py) to upload the local parquet data to our gcp bucket.
```
python etl_web_to_gcs.py
```
you can check the uploaded data in GCP -> your project -> cloud storage -> your bucket.


## [2.2.4 - From Google Cloud Storage to Big Query](https://www.youtube.com/watch?v=Cx5jt-V5sgE&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=21)
**Step 1**<br />
Create wo tasks extract_from_gcs(E) and transform(T) to make sure it download and fill missing data as expected.

**Step 2**<br />
Create a Biq Query database in GCP. We have already done this in week 1 using Terraform with database name trips_data_all.<br />
Now we can create a data table manually with the similar information as below using the parquet data we uploaded to GCS bucket.
![bq_create_table1.png](./img/bq_create_table1.png)

You can now run the queries very efficiently as below.<br />
![bq_create_table2.png](./img/bq_create_table2.png)

**Step 3**<br />
We can also write a task to crate the bigquery table - write_bq(L)
Please note here we need to use GcpCredentials block we create last time and the following codes suggested.
```
from prefect_gcp import GcpCredentials
gcp_credentials_block = GcpCredentials.load("gcp-zoomcamp-credentials")
```

Now if we drop the table we created manually and then run [*etl_gcs_to_bq.py*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/etl_gcs_to_bq.py)
```
python etl_gcs_to_bq.py
```


## [2.2.5 - Parametrizing Flow & Deployments with ETL into GCS flow](https://www.youtube.com/watch?v=QrDxPjX10iw&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=22)
**Step 1**<br />
A flow can have multiple runs (instances) with different paremeters. Therefore, we run [*parameterized_flow.py*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/parameterized_flow.py) updated from [*etl_web_to_gcs.py*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/etl_web_to_gcs.py) to reuse the same flow to upload 3 different taxi trips datasets to our GCS Bucket.
Please note that here we have a parant flow - etl_parent_flow() and for each month we ran a separate child flow - etl_web_to_gcs(), so in Prefect Orion UI, we can see the subflows, respectively.
![elt_parent_flow_subflow.png](./img/elt_parent_flow_subflow.png)


**Step 2**<br />
To avoid the need for triggering our workflow manually, we can deploy the workflow using Prefect. In the terminal, we run the command shown below, which outputs a YAML file containing the workflow's deployment metadata.
```
prefect deployment build ./parameterized_flow.py:etl_parent_flow -n "Parameterized ETL"
```
Here, we specify the python script file name and the entry point flow, which is etl_parent_flow not the other one - etl_web_to_gcs in the script. We also assign a name - Parameterized ETL to this deployment.<br />
Note this step will also generate a .prefectignore file.


**Step 3**<br />
In the etl_parent_flow-deployment.yaml generated, we can update the parameters to include inputs.
```
parameters : { "color": "yellow", "months": [1, 2, 3], "year": 2021 }
```
Then we can apply this yaml file to send all the metadata to Prefect API so that it knows we are scheduling this flow.
```
prefect deployment apply etl_parent_flow-deployment.yaml
```
Now if you check Prefect -> Deployment, you will this etl_parent_flow/Parameterized_ETL with a blue switch indicating it is on. You can also switch it off.
![deployment1.png](./img/deployment1.png)
Then if you dive into it, you can add descriptions, see the metadata, and also trigger a quick run and custom run (to modify the parameters). 
![deployment2.png](./img/deployment2.png)


**Step 4**<br />
If we trigger a quick run, in Prefect -> Flow Runs, we will find a new run in schduled state instead of running state.
![schduled_run.png](./img/schduled_run.png)<br />
This is because Prefect knows it is ready to be run, but there is no agent picking up this run.<br />

Agents consist of lightweight Python processes in our execution environment. They pick up scheduled workflow runs from Work Queues.<br />
And work queues coordinate many deployments with many agents by collecting scheduled workflow runs for deployment according to some filtering criteria.
Check here for a better understanding of agents and [work queues](https://docs.prefect.io/concepts/work-queues/)<br />

Now if We launch an agent with the following command. The agent will pulls work from the 'default' work queue to execute flow runs from our deployment.
```
prefect agent start -q 'default'
```
And you will see the status changes from scheduled to pending, to running and finally to completed.


**Step 5**<br />
Here we have tested our codes, but in the future, if you have new scripts, you may want to create a notification in case that the codes may fail. <br />
Or you just want to keep updated when there is a new flow running.
![notification.png](./img/notification.png)



## [2.2.6 - Schedules & Docker Storage with Infrastructure](https://www.youtube.com/watch?v=psNSzqTsi-s&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=23)
**1. Scheduling Flows** 
* Scheduling on Orion UI<br />
Suppose we want our workflow to run every 5 minutes. We can do that in Orion UI by clicking on our deployment and on "Add" under "Schedule".<br />
Then you can change the value/start date .etc to customize your schedule.<br />
![schedule1.png](./img/schedule1.png)<br />
Then after 5 mins, you will find a scheduled parent flow run followed by 3 subflow runs for each of the month of the parameters in the yaml.<br />
![schedule2.png](./img/schedule2.png)

* Scheduling when creating Deployments (via CLI)<br />
Using the code below, we can build and apply a new deployment named etl2 with a specified schedule in type cron - which means run at 12:00 AM every day
    ```
    prefect deployment build parameterized_flow.py:etl_parent_flow -n etl2 --cron "0 0 * * *" -a
    ```
    Now you will have this new deployment at 12:00AM every day (UTC) and 2 scheduled runs as below. <br /> 
    ![schedule3.png](./img/schedule3.png)

* Scheduling after you've created a Deployment (via CLI)<br />
    You can run the following code the get help with deployment
    ```
    prefect deployment --hep
    prefect set-schedule --hep
    ```
    For example, here we learn that we can use the following code the create a new schedule to run at 01:00 AM every day
    ```
    prefect deployment set-schedule etl-parent-flow/etl2 --cron "0 1 * * *"
    ```
    ![schedule4.png](./img/schedule4.png)


**2. Run Flows on Docker Containers** 
We can put our flow code storage in a lot of different places. Before, we had it running on our local machine. But if we want to have other people be able to access our flow code, we can put it on version control systems e.g. GitHub, or cloud storages e.g. AWS S3, Google Cloud Storage, Azure blob storage. <br />
Another option we use here to make our workflows production-ready is to store our code in a Docker image, then put it on Docker Hub, and if we run a Docker container, the code will be right there. <br />


**Step 1. Docker Containers: Dockerfile, Build and Publish **<br />
First, we write a Dockerfile for our workflow, then login to DockerHub, create an image repository, and finally push the image. In the commands, change "hanyingyan" to your DockerHub username.
```
docker image build --no-cache -t hanyingyan/prefect:zoom .
docker login
docker image push hanyingyan/prefect:zoom
```
Now if you got to DockerHub, you will find a repo similar as below<br />
![dockerhub.png](./img/dockerhub.png)


**Step 2**<br />
We need to create a Docker infrastructure block. I assigned "docker-zoom" to block name and set Image to "hanyingyan/prefect:zoom", ImagePullPolicy to "Always" and Auto Remove to true.<br />
![docker_container.png](./img/docker_container.png)<br />
You can also use this code [*make_docker_block.py*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/make_docker_block.py) to create block, just make sure to update the image and docker name you want to use.<br />
Now you can use the block as below.
```
from prefect.infrastructure.docker import DockerContainer
docker_container_block = DockerContainer.load("docker-zoom")
```


**Step 3**<br />
Create deployment. This time, we deploy our container using Python code, see [*docker_deploy.py*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/docker_deploy.py).<br />
```
python docker_deploy.py
```
![docker_deployment.png](./img/docker_deployment.png)

```
prefect profile ls
```
You will most likely have the only one profile default.<br />
Then you can view and change the settings for the current profile.<br />
```
prefect config view
prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```
Now your docker container will be able to interface with Prefect Orion UI.<br />

Now we can fire an agent and run
```
prefect agent start -q default
prefect deployment run etl-parent-flow/docker-flow -p "months=[2, 3]"
```


**Problems during Step 3**
I encountered two errors during step 3 as blow.

* Problem 1
    ```
    Finished in state Failed('Flow run encountered an exception. ValueError: Path /Users/hanying/.prefect/storage/282f1fe3bbc24ca5879cf7726ceb4190 does not exist.\n')
    ```
    This has something to do with the task caching parameters that we set in the function fetch in parameterized_flow.py. The easiest solution to this problem is to remove cache_key_fn and cache_expiration parameters.


* Problem 2
    ```
    pydantic.error_wrappers.ValidationError: 1 validation error for GcsBucket gcp_credentials -> service_account_file
    The provided path to the service account is invalid (type=value_error)

    The above exception was the direct cause of the following exception:
    ...
    RuntimeError: Unable to load 'zoomcamp-gcs' of block type None due to failed validation. To load without validation, try loading again with `validate=False`.

    ```
    This is because when creating the GCS Bucket block, I used a "Service Account File" to set the value of the GCP Credentials block. Then, the JSON file cannot be found by Prefect inside the Docker container. To circumvent this problem, we can just edit our GCP Credentials block and paste the content of our Service Account File as a secret dictionary ("Service Account Info") in the block.


## [2.2.7 - Prefect Cloud/Additional resources](https://www.youtube.com/watch?v=gGC23ZK7lr8&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=25)
[Prefect Doc](https://docs.prefect.io/)<br />
[Prefect Cloud](https://www.prefect.io/cloud/)<br />
[Anna Geller's GitHub](https://github.com/anna-geller)<br />
[Prefect Community](https://discourse.prefect.io/)<br />
