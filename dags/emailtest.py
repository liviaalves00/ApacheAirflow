from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator

default_args = {
    "depends_on_past": False,
    "start_date": datetime(2024, 6, 20),
    "email": ["liviataina.ltab@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=10),
}

dag = DAG(
    "emailtestAGORAVAI",
    description="email",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    default_view="graph",
    tags=["processo", "tag", "pipeline", "email"],
)

task1 = BashOperator(task_id="task1", bash_command="sleep 1", dag=dag)
task2 = BashOperator(task_id="task2", bash_command="sleep 1", dag=dag)
task3 = BashOperator(task_id="task3", bash_command="sleep 1", dag=dag)
task4 = BashOperator(task_id="task4", bash_command="exit 1", dag=dag)
task5 = BashOperator(
    task_id="task5", bash_command="sleep 1", dag=dag, trigger_rule="none_failed"
)
task6 = BashOperator(
    task_id="task6", bash_command="sleep 1", dag=dag, trigger_rule="none_failed"
)

send_email = EmailOperator(
    task_id="send_email",
    to="liviataina.ltab@gmail.com",
    subject="AirflowERROR",
    html_content="""<h3>ERROR DAG!!!</h3>
                          <p>DAG: send_email </p>
                            """,
    dag=dag,
    trigger_rule="one_failed",
)
[task1, task2] >> task3 >> task4
task4 >> [task5, task6, send_email]
