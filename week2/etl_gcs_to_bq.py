from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int):
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("gcp-zoomcamp")
    gcs_block.get_directory(from_path=gcs_path, local_path="./")
    return Path(gcs_path)


@task
def transform(path: Path):
    """Data Cleaning example"""
    df = pd.read_parquet(path)
    print(f"pre:missing passenger count: {df['passenger_count'].isna().sum()}")
    df['passenger_count'].fillna(0, inplace=True)
    print(f"post:missing passenger count: {df['passenger_count'].isna().sum()}")
    return df


@task()
def write_bq(df: pd.DataFrame):
    """Write DataFrame to Big Query"""
    gcp_credentials_block = GcpCredentials.load("gcp-zoomcamp-credentials")

    df.to_gbq(
        destination_table="trips_data_all.rides",
        project_id="dtc-de-373006",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )

@flow()
def etl_gcs_to_bq():
    """Then main ETL function to load data into Big Query"""
    color = "yellow"
    year = 2021
    month =1

    path = extract_from_gcs(color, year, month)
    df = transform(path)
    write_bq(df)

if __name__ == "__main__":
    etl_gcs_to_bq()
    