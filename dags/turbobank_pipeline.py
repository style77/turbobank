import os
import sys
from pendulum import datetime
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig
from airflow.decorators import dag
from airflow.operators.python import PythonOperator

from bank.helpers.simulate_one_day import simulate_one_day

profile_config = ProfileConfig(
    profile_name=os.environ.get("DBT_PROFILE_NAME"),
    target_name=os.environ.get("DBT_TARGET"),
    profiles_yml_filepath=os.environ.get("DBT_PROFILES_PATH"),
)

default_args = {"owner": "airflow", "retries": 1}

TRANSACTION_FEE = 0.01  # external transfer fee
INTERNAL_TRANSACTION_FEE = 0  # internal transfers fee
MAX_TRANSFER = 10000


@dag(start_date=datetime(2024, 1, 1), schedule_interval="@hourly", catchup=False)
def turbobank_pipeline():
    simulate_day = PythonOperator(
        task_id="simulate_transactions",
        python_callable=lambda: simulate_one_day(
            TRANSACTION_FEE, INTERNAL_TRANSACTION_FEE, MAX_TRANSFER
        )
    )

    transform_data = DbtTaskGroup(
        group_id="transform_data",
        project_config=ProjectConfig(os.environ.get('DBT_PROJECT_DIR')),
        profile_config=profile_config,
        operator_args={
            "install_deps": True,  # check if needed, as dbt deps are only used for code generation
        },
        default_args=default_args
    )

    simulate_day >> transform_data


turbobank_pipeline()
