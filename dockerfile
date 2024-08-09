FROM apache/airflow:latest

USER root
RUN apt-get update && \
    apt-get -y install git && \
    apt-get clean

USER airflow
RUN pip install boto3 newspaper3k lxml_html_clean
RUN pip install apache-airflow-providers-amazon

COPY airflow/dags/ /opt/airflow/dags/
COPY aws_credentials /home/airflow/.aws/credentials

ENV AWS_ACCESS_KEY_ID 
ENV AWS_SECRET_ACCESS_KEY 

