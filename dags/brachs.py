import random
from datetime import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator

dag = DAG(
    "branchtest",
    description="brachtest",
    schedule_interval=None,
    start_date=datetime(2024, 6, 20),
    catchup=False,
    default_view="graph",
    tags=["brach", "tag", "pipeline"],
)


def radom_number():
    return random.randint(1, 100)


def even_or_odd(**context):
    value = context["task_instance"].xcom_pull(task_ids="radom_number")
    if value % 2 == 0:
        return "even_task"
    else:
        return "odd_task"


radom_number_task = PythonOperator(
    task_id="radom_number", python_callable=radom_number, dag=dag
)


branch_task = BranchPythonOperator(
    task_id="branch_task",
    python_callable=even_or_odd,
    provide_context=True,
    dag=dag,
)

even_task = BashOperator(
    task_id="even_task", bash_command='echo "Even Number"', dag=dag
)
odd_task = BashOperator(task_id="odd_task", bash_command='echo "Odd Number"', dag=dag)


radom_number_task >> branch_task
branch_task >> even_task
branch_task >> odd_task
