import newspaper
import pandas as pd
import boto3
from io import StringIO

url = 'https://aws.amazon.com/blogs/storage/using-aws-datasync-to-move-data-from-hadoop-to-amazon-s3/'

def parse_article(url):
    article = newspaper.Article(url)
    article.download()
    article.parse()

    article_info = {
        'Title':article.title,
        'Authors': ', '.join(article.authors),
        'Publication Date': article.publish_date,
        'Text': article.text,
        'Top Image': article.top_image,
        'Videos': ','.join(article.movies)
    }

    return article_info

def article_to_df(**kwargs):
    url = kwargs['url']
    bucket_name = kwargs['bucket_name']
    file_name = kwargs['file_name']

    article_data = parse_article(url)

    if isinstance(article_data, dict):
        article_data = [article_data]

    df = pd.DataFrame(article_data)
    print(df)

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_buffer.getvalue())
    print(f"File {file_name} uploaded to S3 bucket {bucket_name}.")

def article_to_snowflake():
    pass

def test_upload_to_s3(**kwargs):
    bucket_name = kwargs['bucket_name']
    file_name = kwargs['file_name']

    s3= boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key=file_name, Body="This is a test!!!")

def df_upload_redshift():
    pass







