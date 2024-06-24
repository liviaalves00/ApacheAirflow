from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
import requests

dag = DAG(
    "httpsensor",
    description="httpsensor",
    schedule_interval=None,
    start_date=datetime(2024, 6, 21),
    catchup=False,
    tags=["httpsensor", "pipeline"],
)


def query_api():
    response = requests.get("https://api.publicapis.org/entries")
    print(response.txt)


check_api = HttpSensor(
    task_id="check_api",
    http_conn_id="connection",
    endpoint="entries",
    poke_interval=5,
    timeout=20,
    dag=dag,
)

process_data = PythonOperator(
    task_id="process_data", python_callable=query_api, dag=dag
)

check_api >> process_data
