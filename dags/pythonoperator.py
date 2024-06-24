import statistics as sts
from datetime import datetime

import pandas as pd

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

dag = DAG(
    "pythonoperator",
    description="pythonoperatortest",
    schedule_interval=None,
    start_date=datetime(2024, 6, 21),
    catchup=False,
    default_view="graph",
    tags=["pythonoperator", "pandas", "pipeline", "statistics"],
)

dataset = pd.read_csv("/opt/airflow/data/Churn.csv", sep=";")
dataset.columns = [
    "Id",
    "Score",
    "State",
    "Gender",
    "Age",
    "Patrimony",
    "Balance",
    "Products",
    "Card",
    "Active",
    "Salary",
    "Exit",
]


def data_cleanner_salary(dataset):
    median = sts.median(dataset["Salary"])
    dataset["Salary"].fillna(median, inplace=True)
    # dataset["Gender"].fillna("Male", inplace=True)


def data_cleanner_age(dataset):
    median = sts.median(dataset["Age"])
    dataset.loc[(dataset["Age"] < 43) | (dataset["Age"] > 70), "Age"] = median


def drop_duplicate(dataset):
    dataset.drop_duplicates(subset="Id", keep="first", inplace=True)


dataset.to_csv("/opt/airflow/data/Churn_treatment.csv", sep=";", index=False)

# t1 = PythonOperator(
#     task_id="data_cleanner_salary",
#     python_callable=data_cleanner_salary,
#     op_args=[dataset],
#     dag=dag,
# )

t2 = PythonOperator(
    task_id="data_cleanner_age",
    python_callable=data_cleanner_age,
    op_args=[dataset],
    dag=dag,
)
