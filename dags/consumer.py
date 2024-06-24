
import pandas as pd
from datetime import datetime
from airflow import DAG, Dataset
from airflow.operators.python_operator import PythonOperator

mydataset = Dataset("/opt/airflow/data/Churn_new.csv")

dag = DAG(
    "consumer",
    description="consumertest",
    schedule=[mydataset],
    start_date=datetime(2024, 6, 21),
    catchup=False,
    default_view="graph",
    tags=["producer", "pandas", "pipeline"],
)

def my_file():
    dataset = pd.read_csv("/opt/airflow/data/Churn_new.csv", sep=";")
    dataset.to_csv("/opt/airflow/data/Churn_new2.csv", sep=";")

t1 = PythonOperator(task_id="task1", python_callable=my_file, dag=dag,provide_context=True)
t1