from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
import pandas as pd
import os
import sys

# Add include path
sys.path.append("/usr/local/airflow/include")

# from ml_models.train_models import ModelTrainer
# from utils.mlflow_utils import MLflowManager
# from data_validation.validators import DataValidator
# from airflow.sdk.definitions.asset import Asset
# from airflow.decorators import dag, task
# from pendulum import datetime
import requests

default_args = {
    "owner": "theanh",
    "depends_on_past": False,
    "start_date": datetime(2025, 7, 22),
    "email_on_failure": True,
    "email_on_retry": False,
    "email": ["admin@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    schedule="@weekly",
    start_date=datetime(2025, 7, 22),
    catchup=False,
    default_args=default_args,
    description="Train sales forecasting models",
    tags=["ml", "training", "sales"],
)
def sales_forecast_training():
    @task()
    def extract_data_task():
        # from include.utils.data_generator import RealisticSalesDataGenerator
        from include.utils.data_genarator import RealisticSalesDataGenerator

        data_output_dir = "/tmp/sales_data"
        generator = RealisticSalesDataGenerator(
            start_date="2021-01-01", end_date="2021-12-31"
        )
        print("Generating realistic sales data...")
        file_paths = generator.generate_sales_data(output_dir=data_output_dir)
        total_files = sum(len(paths) for paths in file_paths.values())
        print(f"Generated {total_files} files:")
        for data_type, paths in file_paths.items():
            print(f"  - {data_type}: {len(paths)} files")
        return {
            "data_output_dir": data_output_dir,
            "file_paths": file_paths,
            "total_files": total_files,
        }
    extract_data = extract_data_task()
    return extract_data

