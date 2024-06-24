from datetime import datetime

from airflow.operators.bash_operator import BashOperator
from airflow.utils.task_group import TaskGroup

from airflow import DAG

dag = DAG(
    "daggroup",
    description="group",
    schedule_interval=None,
    start_date=datetime(2024, 6, 18),
    catchup=False,
)
task1 = BashOperator(task_id="task1", bash_command="sleep 5", dag=dag)
task2 = BashOperator(task_id="task2", bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id="task3", bash_command="sleep 5", dag=dag)
task4 = BashOperator(task_id="task4", bash_command="sleep 5", dag=dag)
task5 = BashOperator(task_id="task5", bash_command="sleep 5", dag=dag)
task6 = BashOperator(task_id="task6", bash_command="sleep 5", dag=dag)
tsk_group = TaskGroup("task_group", dag=dag)
task7 = BashOperator(
    task_id="task7", bash_command="sleep 5", dag=dag, task_group=tsk_group
)
task8 = BashOperator(
    task_id="task8", bash_command="sleep 5", dag=dag, task_group=tsk_group
)
task9 = BashOperator(
    task_id="task9",
    bash_command="sleep 5",
    dag=dag,
    trigger_rule="one_failed",
    task_group=tsk_group,
)
task1 >> task2
task3 >> task4
[task2, task4] >> task5 >> task6
task6 >> tsk_group
