
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket

# alternative to creating GCP blocks in the UI
# insert your own service_account_file path or service_account_info dictionary from the json file
# IMPORTANT - do not store credentials in a publicly available repository!


credentials_block = GcpCredentials(
    #service_account_info={}  # enter your credentials info or use the file method.
    #service_account_file=/Users/hanying/Documents/data-engineering-zoomcamp-hy/dtc-de-373006-58eecc9ef188.json
)

credentials_block = GcpCredentials(

credentials_block.save("gcp-zoomcamp-credentials", overwrite=True)


bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("gcp-zoomcamp-credentials"),
    bucket="dtc_data_lake_dtc-de-373006",  # insert your  GCS bucket name
)

bucket_block.save("gcp-zoomcamp", overwrite=True)