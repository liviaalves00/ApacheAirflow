from datetime import datetime, timedelta

from airflow.operators.bash_operator import BashOperator

from airflow import DAG

default_args = {
    "depends_on_past": False,
    "start_date": datetime(2024, 6, 19),
    "email": ["teste@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=10),
}

dag = DAG(
    "default_args",
    description="dag exemplo",
    default_args=default_args,
    schedule_interval="@hourly",
    start_date=datetime(2024, 6, 19),
    catchup=False,
    default_view="graph",
    tags=["processo", "tag", "pipeline"],
)

task1 = BashOperator(task_id="task1", bash_command="sleep 5", dag=dag, retries=3)
task2 = BashOperator(task_id="task2", bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id="task3", bash_command="sleep 5", dag=dag)

task1 >> task2 >> task3
