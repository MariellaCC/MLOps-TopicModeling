import random
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator, BranchPythonOperator
import datetime
import pandas as pd

my_dag = DAG(
    dag_id='model_retraining',
    tags=['TopicModeling', 'retraining'],
    schedule_interval=datetime.timedelta(seconds=10),
    default_args={
        'owner': 'airflow',
        'start_date': days_ago(0, minute=1)
    },
    catchup=False
)


"""""
import mysql.connector

def calculate_kpi_task():
    # Connect to MySQL
    connection = mysql.connector.connect(
        host='your_mysql_host',
        user='your_username',
        password='your_password',
        database='your_database'
    )
    
    # Create a cursor
    cursor = connection.cursor()
    
    # Execute the query to select the last value from the "metrics" table
    query = "SELECT perplexity FROM metrics ORDER BY id DESC LIMIT 1"
    cursor.execute(query)
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Close the cursor and connection
    cursor.close()
    connection.close()
    
    # Check the value of the perplexity column
    perplexity = result[0]
    if perplexity < 0:
        return 'data_ingestion_task'
    else:
        return 'no_retrain_task'
"""

kpi_metric = 9

def calculate_kpi_task():
    if kpi_metric < 0:
        return 'data_ingestion_task'
    else:
        return 'no_retrain_task'


def data_ingestion_task():
    # Preprocess the data and obtain the subset dataframe
    print("Data ingestion task successful")


def preprocessing_task():
    # Load data
    print("Preprocessing task successful")


def retrain_model_task():
    print("Retrain model task successful")


def no_retrain_task():
    print("No need to retrain as KPI metric is satisfactory")


"""""
from airflow.sensors.sql import SqlSensor
wait_for_new_metric = SqlSensor(
    task_id='wait_for_new_metric',
    conn_id='your_mysql_connection',
    sql="SELECT MAX(id) FROM metrics",
    mode="poke",
    poke_interval=10,  # Interval in seconds to check for new records
    timeout=600  # Maximum time to wait for a new record (in seconds)
)
"""""

check_threshold_task = BranchPythonOperator(
    task_id='check_threshold_task',
    python_callable=calculate_kpi_task,
    dag=my_dag
)

ingestion_task = PythonOperator(
    task_id='data_ingestion_task',
    python_callable=data_ingestion_task,
    dag=my_dag,
    trigger_rule="one_success"
)

pre_processing_task = PythonOperator(
    task_id='pre_processing_task',
    python_callable=preprocessing_task,
    dag=my_dag,
    trigger_rule="one_success"
)

model_retraining_task = PythonOperator(
    task_id='model_retraining_task',
    python_callable=retrain_model_task,
    dag=my_dag,
    trigger_rule="one_success"
)

no_retrain_task = PythonOperator(
    task_id='no_retrain_task',
    python_callable=no_retrain_task,
    dag=my_dag,
    trigger_rule="one_success"
)


check_threshold_task >> [ingestion_task, no_retrain_task]
ingestion_task >> pre_processing_task >> model_retraining_task

""""
wait_for_new_metric >> check_threshold_task >> [ingestion_task, no_retrain_task]
ingestion_task >> pre_processing_task >> model_retraining_task
"""