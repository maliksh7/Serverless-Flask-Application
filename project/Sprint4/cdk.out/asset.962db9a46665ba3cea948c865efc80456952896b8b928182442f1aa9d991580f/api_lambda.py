import datetime
from urllib import response
import urllib3
import constants as constants
import boto3
import json
import logging
import os

from custom_encoder import CustomEncoder
from cloud_watch import CloudWacth

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DynamaodbTableName = os.environ["url_table_name"]
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DynamaodbTableName)

createMethod = "POST"
readMethod = "GET"
updatMethod = "PATCH"
deleteMethod = "DELETE"
urlsPath = "/urls"


def wh_api_handler(event, context):
    
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']

    # -------------------------------------------------------------------------- >>>>>> Done
    if httpMethod == createMethod and path == urlsPath:
                                                                        # use event body for this create method
        requestBody = json.loads(event['body'])
        # requestBody = event['body']
        url_id      =    requestBody["URL_ID"]
        url         =    requestBody["URL"]
        thrushold   =    requestBody["Thrushold"]
        
        response =   createurl(url_id, url, thrushold)

    # -------------------------------------------------------------------------- >>>>>> Done
    elif httpMethod == readMethod and path == urlsPath:
                                                                        # using querStringParameters to get product Id
        url_id        = event["queryStringParameters"]['URL_ID']
        # url_id        = event["body"]['URL_ID']
        # requestBody = json.loads(event['body'])
        # url_id        = requestBody['URL_ID']
        response      =   geturl(url_id)

    # -------------------------------------------------------------------------- >>>>>> Done
    elif httpMethod == updatMethod and path == urlsPath:
                                                                        # Use event body to update
        requestBody =   json.loads(event['body'])
        # requestBody =   event['body']
        url_id  = requestBody["URL_ID"]
        new_url = requestBody["NEW_URL"]
        new_thrushold = requestBody["NEW_Thrushold"]
        
        response    =   updateurl(url_id, new_url, new_thrushold)

    # -------------------------------------------------------------------------- >>>>>> Done
    elif httpMethod == deleteMethod and path == urlsPath:
                                                                        # Use event body to delete
        requestBody = json.loads(event["body"])
        # requestBody = event["body"]
        url_id = requestBody["URL_ID"]
        
        response     = deleteurl(url_id)

    else:
        response    = buildResponse(404, 'Not Found')

    return response


def updateurl(url_id, new_url = None, new_thrushold = None):
    try:
        if new_url is not None:
            response = table.update_item(
                Key={'URL_ID': url_id},
                UpdateExpression='SET URLS = :val1',
                ExpressionAttributeValues={':val1': new_url},
                ReturnValues="UPDATED_NEW"
                )
        
        if new_thrushold is not None:
            response = table.update_item(
                Key={'URL_ID': url_id},
                UpdateExpression='SET Thrushold = :val1',
                ExpressionAttributeValues={':val1': new_thrushold},
                ReturnValues="UPDATED_NEW"
                )
        
        
        body = {
            'Operation' : "Update",
            "Message"   : "SUCCESS",
            "Item"      : response
            }
        
        return buildResponse(200, body)

    except:
        logger.exception('Do your custom error handling here. I am logging out.')
        
        
        



def createurl(url_id, url, thrushold):
    
    try:
        Item={
                "URL_ID": url_id,
                "URLS": url,
                "Thrushold": thrushold,
            }
        response=table.put_item(
            Item=Item
        )
        
        body = {
            'Operation' : "Save",
            "Message"   : "SUCCESS",
            "Item"      : Item
        }
        
        return buildResponse(200, body)

    except:
        logger.exception('Do your custom error handling here. I am logging out.')




def geturl(url_id):
    try:
        response = table.get_item(
            Key={
                "URL_ID": url_id,
                }
                )
        # item=response['Item']

        if "Item" in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {'Message': "URL %s not find " % url_id})

    except:
        logger.exception(
            'Do your custom error handling here. I am logging out.')


def deleteurl(url_id):
    try:
        response=table.delete_item(
            Key={
                "URL_ID": url_id,
                },
            ReturnValues = "ALL_OLD",
                )
        body = {
            'Operation' : "Delete",
            "Message"   : "SUCCESS",
            "Item"      : response
        }
        
        return buildResponse(200, body)

    except:
        logger.exception('Do your custom error handling here. I am logging out.')




def buildResponse(statusCode, body=None):
    response={
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain',
            'Access-Control-Allow-Origion': '*'
        }
    }
    if body is not None:
                                        # Becasue the object we get from dynamodb is in decimal which is not sported by default json encoder, So we define a Custom Encoder.
        response['body']=json.dumps(body, cls=CustomEncoder)
    return response