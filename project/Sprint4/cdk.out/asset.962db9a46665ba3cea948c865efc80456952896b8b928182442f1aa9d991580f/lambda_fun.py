# import os
# import json
# import boto3
# from custom_encoder import CustomEncoder
# import logging
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)

# dynamoTableName = 'Saad_webCrawler'
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table(dynamoTableName)

# #define methods
# getMethod = 'GET'
# postMethod = 'POST'
# patchMethod = 'PATCH'
# deleteMethod = 'DELETE'

# #define paths
# healthPath = '/health'
# urlsPath = '/urls'
# urlPath = '/url'
import datetime
from urllib import response
import urllib3
# import constants as constants
import boto3
import json
import logging
import os

from custom_encoder import CustomEncoder
# from cloud_watch import CloudWacth

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DynamaodbTableName = os.environ["bktTotable"]
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DynamaodbTableName)

createMethod = "POST"
readMethod = "GET"
updatMethod = "PATCH"
deleteMethod = "DELETE"
urlsPath = "/urls"


def lambda_handler(event, context):
    # # log the request event
    # logger.info(event)
    
    # # extract the http method from event object
    # httpMethod = event['httpMethod']
    
    # # extract the path from event object
    # path = event['path']
    
    # if httpMethod == getMethod and path == healthPath:
    #     response = buildResponse(200)
    
    # elif httpMethod == getMethod and path == urlPath:
    #     response = getUrl(event['queryStringParameters']['urlId'])

    # elif httpMethod == getMethod and path == urlsPath:
    #     response = getUrls()

    # elif httpMethod == postMethod and path == urlPath:
    #     response = saveUrl(json.load(event['body']))

    # elif httpMethod  == patchMethod and path == urlPath:
    #     requestBody = json.load(event['body'])
    #     response = modifyUrl(requestBody['urlId'], requestBody['updateKey'], requestBody['updateVaue'])

    # elif httpMethod == deleteMethod and path == urlPath:
    #     requestBody = json.load(event['body'])
    #     response = deleteUrl(requestBody['urlId'])

    # else:  
    #     response = buildResponse(404, 'Not Found')

    # return response
    
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
    
    
# def getUrls():
#     try:
#         response = table.scan()
#         result = response['Items']
        
#         while 'LastEvaluatedKey' in response:
#             response = table.scan(ExclusiveStartKey = response['LastEvaluatedKey'])
#             result.extend(response['Items'])
            
#         body = {
#             'urls' : result
#         }
        
#         return buildResponse(200, body)
        
#     except:
#         logger.exception('[* ] - Exception Occured, Do custom error handling!!!')
    
# def getUrl(urlId):
#     try:
#         response = table.get_item(
#             Key = {
#                 'urlId': urlId
#             }
#         )
        
#         if 'Item' in response:
#             return buildResponse(200, response['Item'])
            
#         else:
#             return buildResponse(404, {'Message': 'UrlId: %s not found' % urlId})
            
#     except:
#         logger.exception('[* ] - Exception Occured, Do custom error handling!!!') 

# def saveUrl(requestBody):
#     try:
#         table.put_item(Item=requestBody)
#         body = {
#             'Operation': 'SAVE',
#             'Message': 'SUCCESS',
#             'Item': requestBody
#         }
        
#         return buildResponse(200, body)
        
#     except:
#         logger.exception('[* ] - Exception Occured, Do custom error handling!!!')
        

# def modifyUrl(urlId, updateKey, updateValue):
#     try:
#         response = table.update_item(
#             Key = {
#                 'urlId': urlId
#             },
#             UpdateExpression = 'set %s = :value' % updateKey,
#             ExpressionAttributeValues = {
#                 ':value': updateValue
#             },
#             ReturnValues = 'UPDATED_NEW'
#         )
        
#         body = {
#             'Operation': 'UPDATED',
#             'Message': 'SUCCESS',
#             'UpdatedAttributes': response
#         }
        
#         return buildResponse(200, body)
#     except:
#         logger.exception('[* ] - Exception Occured, Do custom error handling!!!') 
       

# def deleteUrl(urlId):
#     try:
#         response = table.delete_item(
#             Key = {
#                 'urlId': urlId
#             },
#             ReturnValues = 'ALL_OLD'
            
#         )
        
#         body = {
#             'Operation': 'DELETE',
#             'Message': 'SUCCESS',
#             'deletedItem': response
#         }
        
#         return buildResponse(200, body)
#     except:
#         logger.exception('[* ] - Exception Occured, Do custom error handling!!!') 

  

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






""" buid a response """
def buildResponse(statusCode, body = None):
    response = {
        'statusCode': statusCode,
        'header': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
    return response
    
