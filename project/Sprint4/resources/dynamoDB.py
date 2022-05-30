import json
import boto3
import os

'''Writing Data to the DynamoDB Table'''

def lambda_handler(event, context):
    
    # get alarm table name from environment
    alarmTableName= os.environ["tableName"]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(alarmTableName)

    # parse data from topic subscription to insert it in database 

    table.put_item(
            Item={
                    "Timestamp": event["Records"][0]["Sns"]["Timestamp"],
                    "Subject": event["Records"][0]["Sns"]["Subject"]
                })
