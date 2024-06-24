from datetime import datetime

from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from airflow import DAG

dag = DAG(
    "xcom_example",
    description="xcom",
    schedule_interval=None,
    start_date=datetime(2024, 6, 19),
    catchup=False,
)


def task_write(**kwarg):
    kwarg["ti"].xcom_push(key="xcomvalue1", value=10200)


task1 = PythonOperator(
    task_id="task1", python_callable=task_write, provide_context=True, dag=dag
)


def task_read(**kwarg):
    value = kwarg["ti"].xcom_pull("xcomvalue1")
    print(f"value recive: {value}")


task2 = PythonOperator(
    task_id="task2", python_callable=task_read, provide_context=True, dag=dag
)

task1 >> task2
