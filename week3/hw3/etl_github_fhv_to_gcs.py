from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(retries=3)#, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str):
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    return df


@task(log_prints=True)
def clean(df = pd.DataFrame):
    """Fix dtype issues"""
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    df['dropOff_datetime'] = pd.to_datetime(df['dropOff_datetime'])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str):
    """Write DataFrame out locally as gz file"""
    from_path = Path(f"/Users/hanying/Documents/data-engineering-zoomcamp-hy/week3/data/{color}/{dataset_file}.csv.gz")
    to_path = Path(f"data/{color}/{dataset_file}.csv.gz")
    df.to_csv(from_path, compression="gzip")
    return from_path, to_path


@task()
def write_gcs(from_path: Path, to_path: Path):
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("gcp-zoomcamp")
    gcs_block.upload_from_path(from_path=from_path, to_path=to_path)


@flow()
def etl_web_to_gcs(year: int, month: int, color: str):
    """Then main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    from_path, to_path = write_local(df_clean, color, dataset_file)
    write_gcs(from_path, to_path)


@flow()
def etl_parent_flow(months: list[int] = [1], year: int = 2019, color: str = "fhv"):
    for month in months:
        etl_web_to_gcs(year, month, color)

if __name__ == "__main__":
    color = "fhv"
    year = 2019
    months = [1, 2]
    etl_parent_flow(months, year, color)