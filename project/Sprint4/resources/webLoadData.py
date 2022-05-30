from decimal import Decimal
import json
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# import webcheck


import boto3

'''Web URL Data'''
def webURLS_handler(event, context):
    response = saveUrl(json.load(event['body']))
    return response
    
    
def saveUrl(requestBody):
    try:
        table.put_item(Item=requestBody)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': requestBody
        }
        
        return body
        
    except:
        logger.exception('[* ] - Exception Occured, Do custom error handling!!!')
        
# class webURLS:

#     def load_urls(self, urls, dynamodb=None):
#         if not dynamodb:
#             dynamodb = boto3.resource('dynamodb', 
#             # endpoint_url="http://localhost:8000"
#             )
    
#         table = dynamodb.Table('Saad_webCrawler')
        
#         # for num, name in enumerate(presidents, start=1):
#         #     print("President {}: {}".format(num, name))
        
#         web_url = None
#         c = 0
#         for url in urls:
#             url_name = url
#             print("Adding Web URL:", url_name)
#             web_url = table.put_item(Item={
#             'id': c,
#             'Url': url[0]
#             })
#             c += 1
            
#         return web_url
    




# if __name__ == '__main__':
    
#     # with open("moviedata.json") as json_file:
#     urls_list = json.load(webcheck.URLS_TO_MONITOR, parse_float=Decimal)
#     d = webURLS()
#     d.load_urls(urls_list)