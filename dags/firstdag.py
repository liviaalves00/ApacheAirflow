from datetime import datetime

from airflow.operators.bash_operator import BashOperator

from airflow import DAG

dag = DAG(
    "firstdag",
    description="Our second DAG",
    schedule_interval=None,
    start_date=datetime(204, 6, 18),
    catchup=False,
)

task1 = BashOperator(task_id="task1", bash_command="sleep 5", dag=dag)
task2 = BashOperator(task_id="task2", bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id="task3", bash_command="sleep 5", dag=dag)

task1 >> task2 >> task3
