* gcloud auth login<br />
* bq --project_id dtc-de-373006 extract -m trips_data_all.tip_model gs://dtc_data_lake_dtc-de-373006/tip_model<br />
* mkdir /tmp/model<br />
* gsutil cp -r gs://dtc_data_lake_dtc-de-373006/tip_model /tmp/model<br />
* mkdir -p serving_dir/tip_model/1<br />
* cp -r /tmp/model/tip_model/* serving_dir/tip_model/1<br />
* docker pull tensorflow/serving<br />
* docker run -p 8501:8501 --mount type=bind,source=/Users/hanying/Documents/data-engineering-zoomcamp-hy/week3/serving_dir/tip_model,target=/models/tip_model -e MODEL_NAME=tip_model -t tensorflow/serving &<br />
* curl -d '{"instances": [{"passenger_count":1, "trip_distance":12.2, "PULocationID":"193", "DOLocationID":"264", "payment_type":"2","fare_amount":20.4,"tolls_amount":0.0}]}' -X POST http://localhost:8501/v1/models/tip_model:predict<br />
* http://localhost:8501/v1/models/tip_model<br />
