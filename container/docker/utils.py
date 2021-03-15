import boto3
import tarfile
from urllib.parse import urlparse

s3 = boto3.client('s3')


def get_model_bucket_key(model_s3_uri):
    o = urlparse(model_s3_uri)
    bucket = o.netloc
    key = o.path
    return bucket, key


def extract_model(model_s3_uri, extract_folder):
    try:
        filename = '/tmp/model.tar.gz'
        bucket, key = get_model_bucket_key(model_s3_uri)
        s3.download_file(bucket, key[1:], filename)

        tar = tarfile.open(filename)
        tar.extractall(extract_folder)
        tar.close()
    except Exception as e:
        raise e