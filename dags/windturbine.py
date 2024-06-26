from email.policy import default
from pkgutil import get_data
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.email_operator import EmailOperator
from airflow.sensors.filesystem import FileSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
import airflow.models
from airflow.models import Variable
from airflow.utils.task_group import TaskGroup
import json
import os

default_args = {
    "depends_on_past": False,
    "email": ["liviataina.ltab@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=10),
}
# schedule_interval='*/3 * * * *'
dag = DAG(
    "windturbine",
    description="Wind Turbine DAG",
    schedule_interval=None,
    start_date=datetime(2024, 6, 24),
    catchup=False,
    default_args=default_args,
    default_view="graph",
    doc_md="## Wind Turbine DAG",
    tags=["windturbine"],
)

group_check_temp = TaskGroup(group_id="group_check_temp", dag=dag)
group_database = TaskGroup(group_id="group_database", dag=dag)


# to do: otimizar a função para apagar e pegar. novamente o aruivo
def process_file(**kwarg):
    with open(Variable.get("path_file_json"), "r") as file:
        data = json.load(file)
        kwarg["ti"].xcom_push(key="idtemp", value=data["idtemp"])
        kwarg["ti"].xcom_push(key="powerfactor", value=data["powerfactor"])
        kwarg["ti"].xcom_push(key="hydraulicpressure", value=data["hydraulicpressure"])
        kwarg["ti"].xcom_push(key="temperature", value=data["temperature"])
        kwarg["ti"].xcom_push(key="timestamp", value=data["timestamp"])
    os.remove(Variable.get("path_file_json"))


def check_temperature(**context):
    temperature = float(context["ti"].xcom_pull(task_ids="get_data", key="temperature"))
    if temperature >= 24:
        return "group_check_temp.send_email_alert"
    return "group_check_temp.send_email_normal"


file_sensor_task = FileSensor(
    task_id="file_sensor_task",
    filepath=Variable.get("path_file_json"),
    fs_conn_id="fs_default",
    poke_interval=10,
    dag=dag,
)

get_data = PythonOperator(
    task_id="get_data", python_callable=process_file, provide_context=True, dag=dag
)

create_table = PostgresOperator(
    task_id="create_table",
    postgres_conn_id="postgres",
    sql="""
        CREATE TABLE IF NOT EXISTS sensors (
            idtemp varchar PRIMARY KEY,
            powerfactor varchar,
            hydraulicpressure varchar,
            temperature varchar,
            timestamp varchar
        );
    """,
    task_group=group_database,
    dag=dag,
)

insert_data = PostgresOperator(
    task_id="insert_data",
    postgres_conn_id="postgres",
    parameters={
        "idtemp": '{{ ti.xcom_pull(task_ids="get_data", key="idtemp") }}',
        "powerfactor": '{{ ti.xcom_pull(task_ids="get_data", key="powerfactor") }}',
        "hydraulicpressure": '{{ ti.xcom_pull(task_ids="get_data", key="hydraulicpressure") }}',
        "temperature": '{{ ti.xcom_pull(task_ids="get_data", key="temperature") }}',
        "timestamp": '{{ ti.xcom_pull(task_ids="get_data", key="timestamp") }}',
    },
    sql="""
        INSERT INTO sensors (idtemp, powerfactor, hydraulicpressure, temperature, timestamp)
        VALUES (%(idtemp)s, %(powerfactor)s, %(hydraulicpressure)s, %(temperature)s, %(timestamp)s)
        ON CONFLICT (idtemp)
        DO UPDATE SET
            powerfactor = EXCLUDED.powerfactor,
            hydraulicpressure = EXCLUDED.hydraulicpressure,
            temperature = EXCLUDED.temperature,
            timestamp = EXCLUDED.timestamp;
    """,
    task_group=group_database,
    dag=dag,
)


send_email_alert = EmailOperator(
    task_id="send_email_alert",
    to="liviataina.ltab@gmail.com",
    subject="Airflow Alert",
    html_content="""
        <h3>Temperature Alert</h3>
        <p>DAG: Wondturbine</p>
        <p>Temperature is above the limit</p>
        <p>Something went wrong, please check</p>
    """,
    task_group=group_check_temp,
    dag=dag,
)

send_email_normal = EmailOperator(
    task_id="send_email_normal",
    to="liviataina.ltab@gmail.com",
    subject="Airflow advise",
    html_content="""
        <h3>Temperature Normal</h3>
        <p>DAG: Wondturbine</p>
        <p>Temperature is normal</p>
    """,
    task_group=group_check_temp,
    dag=dag,
)

check_temp_branch = BranchPythonOperator(
    task_id="check_temp_branch",
    python_callable=check_temperature,
    provide_context=True,
    task_group=group_check_temp,
    dag=dag,
)

with group_check_temp:
    check_temp_branch >> [send_email_alert, send_email_normal]

with group_database:
    create_table >> insert_data

file_sensor_task >> get_data
get_data >> group_check_temp
get_data >> group_database
