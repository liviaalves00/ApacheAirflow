from datetime import datetime
import pandas as pd
from airflow import DAG, Dataset
from airflow.operators.python_operator import PythonOperator

dag = DAG(
    "producer",
    description="producertest",
    schedule_interval=None,
    start_date=datetime(2024, 6, 21),
    catchup=False,
    default_view="graph",
    tags=["producer", "pandas", "pipeline"],
)

mydataset = Dataset("/opt/airflow/data/Churn_new.csv")

def my_file():
    dataset = pd.read_csv("/opt/airflow/data/Churn.csv", sep=";")
    dataset.to_csv("/opt/airflow/data/Churn_new.csv", sep=";")
#outlets=[mydataset] == avisa que o dataset está sendo atualizado
t1 = PythonOperator(task_id="task1", python_callable=my_file, dag=dag, outlets=[mydataset])

t1