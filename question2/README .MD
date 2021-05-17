This application extract data from postgres (CSV) and push it into mongo(JSON):

1- make sure that you have all these libraries downloaded
json, logging, pandas, datetime, airflow, pymongo
if you didn't have any one of them you can use this command
pip3 install <library_name>

2- mkdir dags (will contain the dag.py ),
data (it will contain the input.csv and the ouput.json ),
logs (it will contain the airflow logs),
plugins (it will contain files during running the workflow)

3- initialize the workflow
docker-compose up -d airflow-init

4-get the docker compose up
docker-compose up -d

5- sql to container then excute the sql qurey
docker cp ./sql.sql de_postgres:/file.sql
docker cp ./loan_data_set.csv de_postgres:/file.csv
docker exec -u postgres de_postgres psql postgres postgres -f /file.sql
docker exec airflow_web mkdir -p /home/airflow/data

6- go to file dags that contain "dag.py" and run it

7- you can now access Airflow on "localhost:8080"
then you will have "Assignment1_Q2" DAG , run it

8- you will find the json file in the data file, you can also access the mongo-express on port 8081 to see
the json file pushed to mongo
