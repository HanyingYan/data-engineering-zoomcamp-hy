from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from random import randint


@task(retries=3)
def fetch(dataset_url: str):
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    # convert to desired datatype
    df = df.astype({
                    'VendorID': 'Int64',
                    'tpep_pickup_datetime': 'datetime64',
                    'tpep_dropoff_datetime': 'datetime64',
                    'passenger_count': 'Int64',
                    'trip_distance': 'float64',
                    'RatecodeID': 'Int64',
                    'store_and_fwd_flag': 'object',
                    'PULocationID': 'Int64',
                    'DOLocationID': 'Int64',
                    'payment_type': 'Int64',
                    'fare_amount': 'float64',
                    'extra': 'float64',
                    'mta_tax': 'float64',
                    'tip_amount': 'float64',
                    'tolls_amount': 'float64',
                    'improvement_surcharge': 'float64',
                    'total_amount': 'float64',
                    'congestion_surcharge': 'float64'
                    })
    return df


@task(log_prints=True)
def clean(df = pd.DataFrame):
    """Fix dtype issues"""
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str):
    """Write DataFrame out locally as parquet file"""
    from_path = Path(f"/Users/hanying/Documents/data-engineering-zoomcamp-hy/week4/data/{color}/{dataset_file}.parquet")
    to_path = Path(f"data/{color}/{dataset_file}.parquet")
    df.to_parquet(from_path, compression="gzip")
    return from_path, to_path


@task()
def write_gcs(from_path: Path, to_path: Path):
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("gcp-zoomcamp")
    gcs_block.upload_from_path(from_path=from_path, to_path=to_path)


@flow()
def etl_web_to_gcs_yellow(year: int, month: int, color: str):
    """Then main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df)
    from_path, to_path = write_local(df_clean, color, dataset_file)
    write_gcs(from_path, to_path)


@flow()
def etl_parent_flow_yellow(months: list[int] = [1], year: int = 2019, color: str = "yellow"):
    for month in months:
        etl_web_to_gcs_yellow(year, month, color)

if __name__ == "__main__":
    color = "yellow"
    year = 2020
    months = [1]
    etl_parent_flow(months, year, color)