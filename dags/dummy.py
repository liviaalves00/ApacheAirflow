from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

dag = DAG(
    "dummy",
    description="dummytest",
    schedule_interval=None,
    start_date=datetime(2024, 6, 20),
    catchup=False,
    default_view="graph",
    tags=["dummy", "tag", "pipeline"],
)

task1 = BashOperator(task_id="task1", bash_command="sleep 1", dag=dag)
task2 = BashOperator(task_id="task2", bash_command="sleep 1", dag=dag)
task3 = BashOperator(task_id="task3", bash_command="sleep 1", dag=dag)
task4 = BashOperator(task_id="task4", bash_command="sleep 1", dag=dag)
task5 = BashOperator(task_id="task5", bash_command="sleep 1", dag=dag)
taskdummy = DummyOperator(task_id="taskdummy", dag=dag)

[task1, task2, task3] >> taskdummy >> [task4, task5]
