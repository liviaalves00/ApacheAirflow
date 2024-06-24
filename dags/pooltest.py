from datetime import datetime, timedelta
from multiprocessing import pool

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

dag = DAG(
    "pool",
    description="pooltest",
    schedule_interval=None,
    start_date=datetime(2024, 6, 20),
    catchup=False,
    default_view="graph",
    tags=["pool", "tag", "pipeline"],
)

task1 = BashOperator(
    task_id="task1", bash_command="sleep 5", dag=dag, pool="pool", priority_weight=3
)
task2 = BashOperator(task_id="task2", bash_command="sleep 5", dag=dag, pool="pool")
task3 = BashOperator(
    task_id="task3", bash_command="sleep 5", dag=dag, pool="pool", priority_weight=10
)
task4 = BashOperator(task_id="task4", bash_command="sleep 5", dag=dag, pool="pool")
