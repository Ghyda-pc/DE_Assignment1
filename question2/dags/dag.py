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
    def id(**kwargs):
        id = uuid.uuid4()
        LOGGER.info('id: ' + str(id))
        ti = kwargs['ti']
        ti.xcom_push(key='file_id', value=str(id))

    def tojson(**kwargs):
        ti = kwargs['ti']
        id = ti.xcom_pull(key='file_id', task_ids=['id'])[0]
        df = pd.read_csv('/home/airflow/data/' + str(id) + '.csv')
        df.reset_index(inplace=True)
        dict = df.to_dict("records")
        LOGGER.info(str(dict))
        with open('/home/airflow/data/' + str(id) + '.json', 'w') as file:
            json.dump(dict, file)
        LOGGER.info('done')

    def toMongo(**kwargs):
            ti = kwargs['ti']
            id = ti.xcom_pull(key='file_id', task_ids=['id'])[0]
            client = MongoClient("mongodb://mongoadmin:mongo@de_mongo:27017")
            db = client["loan"]
            Collection = db["loan_data_set"]
            with open('/home/airflow/data/' + str(id) + '.json') as file:
                file_data = json.load(file)
                Collection.insert_many(file_data)

    Id = PythonOperator(
        task_id='Id',
        python_callable=id,
        provide_context=True,
        dag=dag)
    CSV = BashOperator(
        task_id='CSV',
        bash_command='psql postgresql://postgres:postgres@de_postgres:5432 -c "\copy loan_data_set to \'/home/airflow/data/{{ti.xcom_pull(key="file_id", task_ids=["id"])[0]}}.csv\' csv header ;"',
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
