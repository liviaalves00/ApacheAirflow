from datetime import datetime

from airflow.operators.bash_operator import BashOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator

from airflow import DAG

dag = DAG(
    "dagrundag1",
    description="Dag run dag",
    schedule_interval=None,
    start_date=datetime(2024, 6, 19),
    catchup=False,
)
task1 = BashOperator(task_id="task1", bash_command="sleep 5", dag=dag)
task2 = TriggerDagRunOperator(task_id="task2", trigger_dag_id="dagrundag2", dag=dag)

task1 >> task2
