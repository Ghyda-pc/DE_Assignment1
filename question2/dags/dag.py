import json
import logging
import pandas as pd
from datetime import timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from pymongo import MongoClient
import uuid


LOGGER = logging.getLogger("airflow.task")

default_args = {
    'owner': 'GhaydaHyasat',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)}

with DAG(
        'Assignment1_Q2',
        default_args=default_args,
        start_date=days_ago(5)
) as dag:
#Functions 
    def id(**kwargs):
        id = uuid.uuid4()
        ti = kwargs['ti']
        LOGGER.info('the id: ' + str(id))
        ti.xcom_push(key='file_id', value=str(id))

    def tojson(**kwargs):
        id = ti.xcom_pull(key='file_id', task_ids=['id'])[0]
        ti = kwargs['ti']
        df = pd.read_csv('/home/airflow/data/' + str(id) + '.csv')
        df.reset_index(inplace=True)
        dict = df.to_dict("all_records")
        with open('/home/airflow/data/' + str(id) + '.json', 'w') as file:
            json.dump(dict, file)
        LOGGER.info(str(dict))

    def toMongo(**kwargs):
        id = ti.xcom_pull(key='file_id', task_ids=['id'])[0]
        ti = kwargs['ti']
            client = MongoClient("mongodb://mongoadmin:mongo@de_mongo:27017")
            db = client["loan"]
            Collection = db["loan_data_set"]
            with open('/home/airflow/data/' + str(id) + '.json') as file:
                file_data = json.load(file)
                Collection.insert_many(file_data)
#Opertators
    Id = PythonOperator(
        task_id='Id',
        python_callable=id,
        provide_context=True,
        dag=dag)
    
    CSV = BashOperator(
        task_id='CSV',
        bash_command='psql postgresql://postgres:postgres@postgres:5432 -c "\copy loan_data_set to \'/home/airflow/data/{{ti.xcom_pull(key="file_id", task_ids=["id"])[0]}}.csv\' csv header ;"',
        dag=dag)
    
    toJSON = PythonOperator(
        task_id='toJSON',
        python_callable=tojson,
        provide_context=True,
        dag=dag)
    
    toMongo = PythonOperator(
        task_id='toMongo',
        python_callable=json,
        provide_context=True,
        dag=dag)

    Id >> CSV >> toJSON >> toMongo
