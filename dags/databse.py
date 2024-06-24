from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

dag = DAG(
    "database",
    description="database",
    schedule_interval=None,
    start_date=datetime(2024, 6, 24),
    catchup=False,
    tags=["database", "pipeline"],
)


def print_result(ti):
    task_instance = ti.xcom_pull(task_ids="query_data")
    print("Query result: ")
    for row in task_instance:
        print(row)


create_table = PostgresOperator(
    task_id="create_table",
    postgres_conn_id="postgres",
    sql="create table if not exists test(id int);",
    dag=dag,
)

insert_data = PostgresOperator(
    task_id="insert_data",
    postgres_conn_id="postgres",
    sql="insert into test values(1);",
    dag=dag,
)

query_data = PostgresOperator(
    task_id="query_data",
    postgres_conn_id="postgres",
    sql="select * from test;",
    dag=dag,
)

print_result_task = PythonOperator(
    task_id="print_result_task", python_callable=print_result, dag=dag
)

create_table >> insert_data >> query_data >> print_result_task
