import boto3
import os
import json
import string
import random
import sys


# downloading file from the created bucket using boto3 client
s3 = boto3.client('s3')
s3.download_file(os.environ['bucketName'], 'webcheck.py', '/tmp/webcheck.py')

# giving path of the imported file
sys.path.insert(1, '/tmp')

import webcheck


def bucket_to_dbHandler(event, context):

    dynamodb = boto3.resource('dynamodb')
    bucktToTableName =  os.environ['S3Totable']
    table = dynamodb.Table(bucktToTableName)
    
    # count = 1
    for url in webcheck.URLS_TO_MONITOR:
        response = table.put_item(TableName=os.environ['S3Totable'],
           Item={
                'id_': "url",
                'url': str(url)
            }
        )