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
    "emailtestallsuccess4",
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
task4 = BashOperator(task_id="task4", bash_command="sleep 1", dag=dag)
task5 = BashOperator(task_id="task5", bash_command="sleep 1", dag=dag)
task6 = BashOperator(task_id="task6", bash_command="sleep 1", dag=dag)

send_email = EmailOperator(
    task_id="send_email",
    to="liviataina.ltab@gmail.com",
    subject="Airflow Success",
    html_content="""<h3>All Tasks Completed Successfully!</h3>
                    <p>Todos as tarefas foram executadas com sucesso.</p>""",
    dag=dag,
    trigger_rule="all_success",  # Alterado para enviar apenas se todas as tarefas forem bem-sucedidas
)

[task1, task2] >> task3 >> task4
task4 >> [task5, task6]
task5 >> send_email
task6 >> send_email  # Adicionando a tarefa 6 ao fluxo de envio de e-mail
