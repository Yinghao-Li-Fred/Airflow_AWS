from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import requests
from extractRawArticle import parse_article, article_to_df, test_upload_to_s3, article_to_snowflake, df_upload_redshift

url = 'https://aws.amazon.com/blogs/storage/using-aws-datasync-to-move-data-from-hadoop-to-amazon-s3/'
bucket_name = 'fred-0522'
file_name = 'article_data.csv'

def print_welcome():
    print('Welcome to Airflow!')

default_args = {
    'owner':'airflow',
    'depends_on_past':False,
    'email_on_failure':False,
    'email_on_retry':False
}

dag = DAG(
    'welcome_dag',
    default_args=default_args,
    description='An example DAG that connects to AWS S3',
    schedule_interval='0 23 * * *',
    start_date=days_ago(1),
    catchup=False
)

print_welcome_task = PythonOperator(
    task_id='print_welcome',
    python_callable=print_welcome,
    dag=dag
)

extract_article = PythonOperator(
    task_id='download_and_parse_article',
    python_callable= parse_article,
    op_kwargs= {'url':url},
    dag=dag
)

df_upload_to_s3 = PythonOperator(
    task_id='print_article',
    python_callable= article_to_df,
    op_kwargs={'url': url, 'bucket_name': bucket_name, 'file_name': file_name},
    dag=dag
)

df_upload_to_snowflake = PythonOperator(
    task_id="upload_to_snowflake",
    python_callable= article_to_snowflake,
    dag=dag
)

upload_to_RedShift = PythonOperator(
    task_id="upload_to_RedShift",
    python_callable= df_upload_redshift,
    dag=dag
)

upload_test = PythonOperator(
    task_id='test_upload',
    python_callable = test_upload_to_s3,
    op_kwargs = {'bucket_name': bucket_name, 'file_name': 'test.txt'},
    dag=dag
)

# Set the dependencies between the tasks
print_welcome_task >> extract_article >> [df_upload_to_s3, df_upload_to_snowflake, upload_test]
df_upload_to_s3 >> upload_to_RedShift

