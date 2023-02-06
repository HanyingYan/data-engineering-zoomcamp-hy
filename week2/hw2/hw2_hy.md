## Week 2 Homework

The goal of this homework is to familiarise users with workflow orchestration and observation. 


## Question 1. Load January 2020 data

Using the `etl_web_to_gcs.py` flow that loads taxi data into GCS as a guide, create a flow that loads the green taxi CSV dataset for January 2020 into GCS and run it. Look at the logs to find out how many rows the dataset has.

How many rows does that dataset have?

* 447,770
* 766,792
* 299,234
* 822,132

----------------------------------
I modified the code and got [*etl_web_to_gcs_green_hy.py*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/hw2/etl_web_to_gcs_green_hy.py) 
```
python hw2/etl_web_to_gcs_green_hy.py
```
where I modified tpep_pickup_datetime to lpep_pickup_datetime, tpep_dropoff_datetime to lpep_dropoff_datetime, and change the input parameter to color = "green", year = 2020, month = 1
logs are
```
10:45:56.557 | INFO    | prefect.engine - Created flow run 'singing-koala' for flow 'etl-web-to-gcs'
10:45:56.704 | INFO    | Flow run 'singing-koala' - Created task run 'fetch-b4598a4a-0' for task 'fetch'
10:45:56.705 | INFO    | Flow run 'singing-koala' - Executing 'fetch-b4598a4a-0' immediately...
/Users/hanying/Documents/data-engineering-zoomcamp-hy/week2/hw2/etl_web_to_gcs_green_hy.py:14: DtypeWarning: Columns (3) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(dataset_url)
10:45:58.999 | INFO    | Task run 'fetch-b4598a4a-0' - Finished in state Completed()
10:45:59.030 | INFO    | Flow run 'singing-koala' - Created task run 'clean-b9fd7e03-0' for task 'clean'
10:45:59.031 | INFO    | Flow run 'singing-koala' - Executing 'clean-b9fd7e03-0' immediately...
10:45:59.274 | INFO    | Task run 'clean-b9fd7e03-0' -    VendorID  ... congestion_surcharge
0       2.0  ...                  0.0
1       2.0  ...                  0.0

[2 rows x 20 columns]
10:45:59.276 | INFO    | Task run 'clean-b9fd7e03-0' - columns: VendorID                        float64
lpep_pickup_datetime     datetime64[ns]
lpep_dropoff_datetime    datetime64[ns]
store_and_fwd_flag               object
RatecodeID                      float64
PULocationID                      int64
DOLocationID                      int64
passenger_count                 float64
trip_distance                   float64
fare_amount                     float64
extra                           float64
mta_tax                         float64
tip_amount                      float64
tolls_amount                    float64
ehail_fee                       float64
improvement_surcharge           float64
total_amount                    float64
payment_type                    float64
trip_type                       float64
congestion_surcharge            float64
dtype: object
10:45:59.276 | INFO    | Task run 'clean-b9fd7e03-0' - rows: 447770
10:45:59.325 | INFO    | Task run 'clean-b9fd7e03-0' - Finished in state Completed()
10:45:59.355 | INFO    | Flow run 'singing-koala' - Created task run 'write_local-f322d1be-0' for task 'write_local'
10:45:59.355 | INFO    | Flow run 'singing-koala' - Executing 'write_local-f322d1be-0' immediately...
10:46:00.786 | INFO    | Task run 'write_local-f322d1be-0' - Finished in state Completed()
10:46:00.837 | INFO    | Flow run 'singing-koala' - Created task run 'write_gcs-1145c921-0' for task 'write_gcs'
10:46:00.838 | INFO    | Flow run 'singing-koala' - Executing 'write_gcs-1145c921-0' immediately...
10:46:00.954 | INFO    | Task run 'write_gcs-1145c921-0' - Getting bucket 'dtc_data_lake_dtc-de-373006'.
10:46:01.842 | INFO    | Task run 'write_gcs-1145c921-0' - Uploading from PosixPath('data/green/green_tripdata_2020-01.parquet') to the bucket 'dtc_data_lake_dtc-de-373006' path 'data/green/green_tripdata_2020-01.parquet'.
10:46:04.528 | INFO    | Task run 'write_gcs-1145c921-0' - Finished in state Completed()
10:46:04.560 | INFO    | Flow run 'singing-koala' - Finished in state Completed('All states completed.')
```
**Answer: 447,770**


## Question 2. Scheduling with Cron

Cron is a common scheduling specification for workflows. 

Using the flow in `etl_web_to_gcs.py`, create a deployment to run on the first of every month at 5am UTC. What’s the cron schedule for that?

- `0 5 1 * *`
- `0 0 5 1 *`
- `5 * 1 0 *`
- `* * 5 1 0`

----------------------------------
```
prefect deployment build parameterized_flow.py:etl_parent_flow -n etl3 -o hw2/q2-deployment.yaml --cron "0 5 1 * *" -a
```
Then I will have a new deployment with Name	- etl-parent-flow/etl3 and Schedule	- At 05:00 AM on day 1 of the month. <br />
**Answer: `0 5 1 * *`**


## Question 3. Loading data to BigQuery 

Using `etl_gcs_to_bq.py` as a starting point, modify the script for extracting data from GCS and loading it into BigQuery. This new script should not fill or remove rows with missing values. (The script is really just doing the E and L parts of ETL).

The main flow should print the total number of rows processed by the script. Set the flow decorator to log the print statement.

Parametrize the entrypoint flow to accept a list of months, a year, and a taxi color. 

Make any other necessary changes to the code for it to function as required.

Create a deployment for this flow to run in a local subprocess with local flow code storage (the defaults).

Make sure you have the parquet data files for Yellow taxi data for Feb. 2019 and March 2019 loaded in GCS. Run your deployment to append this data to your BiqQuery table. How many rows did your flow code process?

- 14,851,920
- 12,282,990
- 27,235,753
- 11,338,483
----------------------------------
First, uploaded the required parquet data files. 
```
prefect deployment run etl-parent-flow/docker-flow -p "months=[2, 3]" -p "year=2019"
```
Then modified the code to get [*parameterized_etl_gcs_to_bq_hy.py*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/hw2/parameterized_etl_gcs_to_bq_hy.py), and created a deployment locally.
```
prefect deployment build  hw2/parameterized_etl_gcs_to_bq_hy.py:etl_gcs_to_bq_parent_flow -n "hw2_q3" -a
```
Finally started a quick run and triggered an agent.

```
prefect agent start -q 'default'
```
logs are
```
Downloading flow code from storage at '/Users/hanying/Documents/data-engineering-zoomcamp-hy/week2'
12:03:34 AM
Created subflow run 'invaluable-sponge' for flow 'etl-gcs-to-bq'
12:03:36 AM
Created subflow run 'olivine-panda' for flow 'etl-gcs-to-bq'
12:04:38 AM
total number of rows processed by the script: 14851920
12:05:41 AM
Finished in state Completed('All states completed.')
```

**Answer: 14851920**


## Question 4. Github Storage Block

Using the `web_to_gcs` script from the videos as a guide, you want to store your flow code in a GitHub repository for collaboration with your team. Prefect can look in the GitHub repo to find your flow code and read it. Create a GitHub storage block from the UI or in Python code and use that in your Deployment instead of storing your flow code locally or baking your flow code into a Docker image. 

Note that you will have to push your code to GitHub, Prefect will not push it for you.

Run your deployment in a local subprocess (the default if you don’t specify an infrastructure). Use the Green taxi data for the month of November 2020.

How many rows were processed by the script?

- 88,019
- 192,297
- 88,605
- 190,225

----------------------------------
Created a github block with name = github-zoom and github repo = https://github.com/HanyingYan/data-engineering-zoomcamp-hy.git<br />
Then I modifed `web_to_gcs` script to get [*parameterized_etl_web_to_gcs_green_hy.py*](https://github.com/HanyingYan/data-engineering-zoomcamp-hy/blob/main/week2/hw2/parameterized_etl_web_to_gcs_green_hy.py)
Then from the root of this repo, we can run 
```
prefect deployment build week2/hw2/parameterized_etl_web_to_gcs_green_hy.py:etl_parent_flow -n "hw2_q4" -sb github/github-zoom -o week2/hw2/etl_parent_flow_github-deployment.yaml --apply
```
Then we can start a quick run and fire an agent

```
prefect agent start -q 'default'
```
The logs are
```
Created task run 'fetch-ba00c645-0' for task 'fetch'
10:33:19 AM
Executing 'fetch-ba00c645-0' immediately...
10:33:19 AM
Finished in state Completed()
10:33:21 AM
fetch-ba00c645-0
Created task run 'clean-2c6af9f6-0' for task 'clean'
10:33:21 AM
Executing 'clean-2c6af9f6-0' immediately...
10:33:21 AM
   VendorID lpep_pickup_datetime  ... trip_type congestion_surcharge
0       2.0  2020-11-01 00:08:23  ...       1.0                 2.75
1       2.0  2020-11-01 00:23:32  ...       1.0                 0.00

[2 rows x 20 columns]
10:33:21 AM
clean-2c6af9f6-0
columns: VendorID                        float64
lpep_pickup_datetime     datetime64[ns]
lpep_dropoff_datetime    datetime64[ns]
store_and_fwd_flag               object
RatecodeID                      float64
PULocationID                      int64
DOLocationID                      int64
passenger_count                 float64
trip_distance                   float64
fare_amount                     float64
extra                           float64
mta_tax                         float64
tip_amount                      float64
tolls_amount                    float64
ehail_fee                       float64
improvement_surcharge           float64
total_amount                    float64
payment_type                    float64
trip_type                       float64
congestion_surcharge            float64
dtype: object
10:33:21 AM
clean-2c6af9f6-0
rows: 88605
10:33:21 AM
clean-2c6af9f6-0
Finished in state Completed()
10:33:21 AM
clean-2c6af9f6-0
Created task run 'write_local-09e9d2b8-0' for task 'write_local'
10:33:21 AM
Executing 'write_local-09e9d2b8-0' immediately...
10:33:21 AM
Finished in state Completed()
10:33:22 AM
write_local-09e9d2b8-0
Created task run 'write_gcs-67f8f48e-0' for task 'write_gcs'
10:33:22 AM
Executing 'write_gcs-67f8f48e-0' immediately...
10:33:22 AM
Getting bucket 'dtc_data_lake_dtc-de-373006'.
10:33:22 AM
write_gcs-67f8f48e-0
Uploading from PosixPath('/Users/hanying/Documents/data-engineering-zoomcamp-hy/week2/data/green/green_tripdata_2020-11.parquet') to the bucket 'dtc_data_lake_dtc-de-373006' path 'data/green/green_tripdata_2020-11.parquet'.
10:33:23 AM
write_gcs-67f8f48e-0
Finished in state Completed()
10:33:24 AM
write_gcs-67f8f48e-0
Finished in state Completed('All states completed.')
```
**Answer: 88605**

## Question 5. Email or Slack notifications

Q5. It’s often helpful to be notified when something with your dataflow doesn’t work as planned. Choose one of the options below for creating email or slack notifications.

The hosted Prefect Cloud lets you avoid running your own server and has Automations that allow you to get notifications when certain events occur or don’t occur. 

Create a free forever Prefect Cloud account at app.prefect.cloud and connect your workspace to it following the steps in the UI when you sign up. 

Set up an Automation that will send yourself an email when a flow run completes. Run the deployment used in Q4 for the Green taxi data for April 2019. Check your email to see the notification.

Alternatively, use a Prefect Cloud Automation or a self-hosted Orion server Notification to get notifications in a Slack workspace via an incoming webhook. 

Join my temporary Slack workspace with [this link](https://join.slack.com/t/temp-notify/shared_invite/zt-1odklt4wh-hH~b89HN8MjMrPGEaOlxIw). 400 people can use this link and it expires in 90 days. 

In the Prefect Cloud UI create an [Automation](https://docs.prefect.io/ui/automations) or in the Prefect Orion UI create a [Notification](https://docs.prefect.io/ui/notifications/) to send a Slack message when a flow run enters a Completed state. Here is the Webhook URL to use: https://hooks.slack.com/services/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

Test the functionality.

Alternatively, you can grab the webhook URL from your own Slack workspace and Slack App that you create. 


How many rows were processed by the script?

- `125,268`
- `377,922`
- `728,390`
- `514,392`
----------------------------------
According to the [slack api](https://api.slack.com/messaging/webhooks), I created personal slack app named hy-hw2-q4, activated incoming webhook and created webhook url https://hooks.slack.com/services/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 to post on channel #prefect-test-webhook. 
Then I created a notification using slack with webhook above, if I run
```
prefect deployment run "etl-parent-flow/hw2_q4" -p "months=[4]" -p "year=2019"
prefect agent start --work-queue "default"
```
I will get logs
```
Created task run 'fetch-ba00c645-0' for task 'fetch'
11:11:59 AM
Executing 'fetch-ba00c645-0' immediately...
11:11:59 AM
Finished in state Completed()
11:12:01 AM
fetch-ba00c645-0
Created task run 'clean-2c6af9f6-0' for task 'clean'
11:12:02 AM
Executing 'clean-2c6af9f6-0' immediately...
11:12:02 AM
   VendorID lpep_pickup_datetime  ... trip_type congestion_surcharge
0         2  2019-04-01 00:18:40  ...         1                 2.75
1         2  2019-04-01 00:18:24  ...         1                 0.00

[2 rows x 20 columns]
11:12:02 AM
clean-2c6af9f6-0
columns: VendorID                          int64
lpep_pickup_datetime     datetime64[ns]
lpep_dropoff_datetime    datetime64[ns]
store_and_fwd_flag               object
RatecodeID                        int64
PULocationID                      int64
DOLocationID                      int64
passenger_count                   int64
trip_distance                   float64
fare_amount                     float64
extra                           float64
mta_tax                         float64
tip_amount                      float64
tolls_amount                    float64
ehail_fee                       float64
improvement_surcharge           float64
total_amount                    float64
payment_type                      int64
trip_type                         int64
congestion_surcharge            float64
dtype: object
11:12:02 AM
clean-2c6af9f6-0
rows: 514392
11:12:02 AM
clean-2c6af9f6-0
Finished in state Completed()
11:12:02 AM
clean-2c6af9f6-0
Created task run 'write_local-09e9d2b8-0' for task 'write_local'
11:12:02 AM
Executing 'write_local-09e9d2b8-0' immediately...
11:12:02 AM
Finished in state Completed()
11:12:04 AM
write_local-09e9d2b8-0
Created task run 'write_gcs-67f8f48e-0' for task 'write_gcs'
11:12:04 AM
Executing 'write_gcs-67f8f48e-0' immediately...
11:12:04 AM
Getting bucket 'dtc_data_lake_dtc-de-373006'.
11:12:04 AM
write_gcs-67f8f48e-0
Uploading from PosixPath('/Users/hanying/Documents/data-engineering-zoomcamp-hy/week2/data/green/green_tripdata_2019-04.parquet') to the bucket 'dtc_data_lake_dtc-de-373006' path 'data/green/green_tripdata_2019-04.parquet'.
11:12:05 AM
write_gcs-67f8f48e-0
Finished in state Completed()
11:12:08 AM
write_gcs-67f8f48e-0
Finished in state Completed('All states completed.')
```
And in slack, I got a notification
```
hanying
  11:17 AM
added an integration to this channel: hy-hw2-q4

hy-hw2-q4
APP  11:19 AM
Prefect flow run notification
Flow run etl-web-to-gcs/ethereal-baboon entered state Completed at 2023-02-06T16:19:56.900699+00:00.
Flow ID: 2dbe6537-0562-4cfd-8a5e-d0fc5d9979b5
Flow run ID: 989a24c6-1819-4691-90a6-76dadbf2479a
Flow run URL: http://ephemeral-orion/api/flow-runs/flow-run/989a24c6-1819-4691-90a6-76dadbf2479a
State message: All states completed.
Prefect NotificationsPrefect Notifications | Today at 11:19 AM
11:19
Prefect flow run notification
Flow run etl-parent-flow/invaluable-yak entered state Completed at 2023-02-06T16:19:56.943056+00:00.
Flow ID: be34e373-a37e-4687-827d-67d7e67c46f3
Flow run ID: 94dcb0c2-92e2-4011-8ebc-427a7d543529
Flow run URL: http://ephemeral-orion/api/flow-runs/flow-run/94dcb0c2-92e2-4011-8ebc-427a7d543529
State message: All states completed.
Prefect NotificationsPrefect Notifications | Today at 11:19 AM
```
**Answer: 514392**

## Question 6. Secrets

Prefect Secret blocks provide secure, encrypted storage in the database and obfuscation in the UI. Create a secret block in the UI that stores a fake 10-digit password to connect to a third-party service. Once you’ve created your block in the UI, how many characters are shown as asterisks (*) on the next page of the UI?

- 5
- 6
- 8
- 10

----------------------------------
I created a Database Credentials blocj with username hanying and 10-digit password 1234567890. Then I got
```
Paste this snippet into your flows to use this block.
from prefect_sqlalchemy import DatabaseCredentials
database_block = DatabaseCredentials.load("hw2-q6")

Copy
Driver
None
Username
hanying
Password
********
Database
None
Host
None
Port
None
Query
None
Url
None
Connect Args
None
```
**Answer: 8**

## Submitting the solutions

* Form for submitting: https://forms.gle/PY8mBEGXJ1RvmTM97
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 6 February (Monday), 22:00 CET


## Solution

We will publish the solution here
