from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator

dag = DAG(
    "variable",
    description="variabletest",
    schedule_interval=None,
    start_date=datetime(2024, 6, 20),
    catchup=False,
    default_view="graph",
    tags=["variable", "tag", "pipeline"],
)


def print_variable(**kwargs):
    print(Variable.get("test_variable"))


task1 = PythonOperator(task_id="task1", python_callable=print_variable, dag=dag)
