import json
import boto3
import os
# import webcheck

client = boto3.client('dynamodb')  # using dynamodb client to put data into the table

'''Writing Data to the DynamoDB Table'''
def lambda_handler(event, context):
    
    
    # Parsing the JSON object
    logID = event['Records'][0]['Sns']['MessageId']
    logType = event['Records'][0]['Sns']['Type']
    messageStr = event['Records'][0]['Sns']['Message']
    message = json.loads(messageStr)
    metricName = message['Trigger']['MetricName']
    nameSpace = message['Trigger']['Namespace']
    alarmName = message['AlarmName']
    url = message['Trigger']['Dimensions'][0]['value']
    timestamp = event['Records'][0]['Sns']['Timestamp']
    
    # Insert item(log) in the Table
    client.put_item(
    TableName=os.environ['tableName'],
    Item={
        'id': { 'S': logID}, 'Type': {'S': logType}, 
        'MetricName': {'S': metricName},'URL': {'S': url}, 
        'NameSpace': { 'S': nameSpace},
        'AlarmName': {'S': alarmName}, 'Timestamp': {'S': timestamp}}
        )
    
    print("Url", url + "MetricName", metricName)
    