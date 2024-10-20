import logging
import boto3
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region=None):
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def list_bucket():
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()
    for bucket in response['Buckets']:
        print(bucket["Name"])

def delete_bucket(bucketName):
    s3_client = boto3.client('s3')
    try:
        s3_client.delete_bucket(Bucket=bucketName)
    except:
        return False

if __name__ == '__main__':
    # create_bucket('test-bucket-from-boto')
    # list_bucket()
    delete_bucket('test-bucket-from-boto')