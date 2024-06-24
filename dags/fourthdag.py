from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

with DAG(
    "fourthddag",
    description="Our fourth DAG",
    schedule_interval=None,
    start_date=datetime(204, 6, 18),
    catchup=False,
) as dag:

    task1 = BashOperator(task_id="task1", bash_command="sleep 5")
    task2 = BashOperator(task_id="task2", bash_command="sleep 5")
    task3 = BashOperator(task_id="task3", bash_command="sleep 5")

# upstream -> task seguinte
# downstream -> task anterior

# task1 >> task2 >> task3 == task1.set_downstream(task2).set_downstream(task3)
task1.set_upstream(task2)
task2.set_downstream(task3)
