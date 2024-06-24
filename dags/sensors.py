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
    response = requests.get("https://catfact.ninja/fact")
    print(response.text)


check_api = HttpSensor(
    task_id="check_api",
    http_conn_id="catfact_connection",  # mesmo nome da conncction criada no airflow
    endpoint="fact",
    poke_interval=5,
    timeout=20,
    dag=dag,
)

process_data = PythonOperator(
    task_id="process_data", python_callable=query_api, dag=dag
)

check_api >> process_data
