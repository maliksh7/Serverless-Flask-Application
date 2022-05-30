from urllib import response
import urllib3
import boto3
import json
import os

from custom_encoder import CustomEncoder

import sys

s3_client = boto3.client('s3')
s3_client.download_file(os.environ['bucketName'],'webcheck.py', '/tmp/webcheck.py')
sys.path.insert(1,'/tmp')
    
import webcheck

getMethod = 'GET' #READ
putMethod = 'PUT' #CREAT
patchMethod = 'PATCH' #UPDATE
deleteMethod = 'DELETE' #DELETE 


#define paths
healthPath = '/health'

urlPath = "/url"

def api_Handler(event, context):
    
    # logger.info(event)
    httpMethod = event["httpMethod"]
    path = event["path"]

    dynamodb = boto3.resource('dynamodb')
    bucktToTableName =  os.environ['S3Totable']
    table = dynamodb.Table(bucktToTableName)
    
    
    if httpMethod == getMethod and path == healthPath:
        response =  {
        "statusCode": 200,
        "body": json.dumps({"statusCode": 200,"httpMethod": httpMethod, "status":"GEt + health", "event['body']":event['body']}),
        "isBase64Encoded": False
        }
        
        return response

    
    # Parse url primary key value & pass to function to read from DB
    elif httpMethod == getMethod and path == urlPath:
        print('event:', json.dumps(event))
        
        l = []

        response = table.scan()
        data = response['Items']
        
        # data is a list of dictionaries
        for i in data:
            l.append(i["url"])
    
        response =  {
        "statusCode": 200,
        "body": json.dumps({"statusCode": 200,"httpMethod": httpMethod,"status":"GEt + url", "event[body]":l}),
        "isBase64Encoded": False
        }
        
        return response
        


    elif httpMethod == putMethod and path == urlPath:
        # response = saveUrl(json.load(event['body']))
        table.put_item(TableName = os.environ['S3Totable'],
                        Item = {
                            "id_": "url",
                            "url" : event['body']
                        })
        response = {
            "statusCode": 200,
            "body": json.dumps({"statusCode": 200, 
                                "event[body]":event['body'],
                                "status":"put + url Inserted",
                                "list":"Values have been inserted"}),
        "isBase64Encoded": False
        }
    
        return response


    

    elif httpMethod  == patchMethod and path == urlPath:
        
        old_url=event['body'].split(',')[0]
        new_url=event['body'].split(',')[1]
        
        InsertedResponse = table.put_item(TableName=os.environ['S3Totable'], Item={'id_': "url",'url': new_url})
          
        delete = table.delete_item(Key={
            
            'id_': 'url',
            'url': old_url
        })
          

        return {
            "statusCode": 200,
            "body": json.dumps({"statusCode": 200, "event[body]":event['body'],
                                "status":"PATCH + url Inserted",
                                "list":new_url + " is added & " +old_url + "is deleted"}),
            "isBase64Encoded": False
            }
 

    elif httpMethod == deleteMethod and path == urlPath:
        response = event['body']
        delete = table.delete_item(Key={
            'id_': 'url',
            'url': response
        })
        return {
            "statusCode": 200,
            "body": json.dumps({"statusCode": 200, "event[body]":response,
                                "status":"deleted url",
                                "list":"Value has been deleted"}),
            "isBase64Encoded": False
            }
    else:  
        response =  {
        "statusCode": 404,
        "body": json.dumps({"statusCode": 404,"httpMethod": httpMethod, "fail":"failure"}),
        "isBase64Encoded": False
        }
        return response
