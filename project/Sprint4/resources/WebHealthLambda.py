import urllib3
import datetime
import os
import boto3  # python sdk
import sys  # importing access keys from a file
from cloudWatch import cloudWatch

# downloading file from the created bucket using boto3 client
s3 = boto3.client('s3')
s3.download_file(os.environ['bucketName'], 'webcheck.py', '/tmp/webcheck.py')

# giving path of the imported file
sys.path.insert(1, '/tmp')


def lambda_handler(event, context):

    import webcheck
    
    # w_url = webURLS()
    cw = cloudWatch()
    # creating an object of class Cloudwatchputmetric()
    values = []
    dim_values = []
    
    dynamodb = boto3.resource('dynamodb')
    bktTotable = os.environ['S3Totable']
    
    table = dynamodb.Table(bktTotable)
    res = table.scan()
    items = res['Items']
    
    for item in items:
        values.append(item["url"])
    
    
    for url in values:
        lst = dict()
        avail = get_availability(url)
        latency = get_latency(url)
        
        #defining dimesions for our metrics
        Dimensions = [                      
            {"Name": "URL", "Value": url}
        ]
        
        """ creating metrics """
        
        # data for availability metric
        cw.put_data(webcheck.URL_NAMESPACE, webcheck.METRIC_NAME_AVAIL, Dimensions,
                    avail)  
        
        # data for latency metric
        cw.put_data(webcheck.URL_NAMESPACE, webcheck.METRIC_NAME_LAT, Dimensions,
                    latency)  
        
        """ creating alarms """      
    
        cw.create_alarm(name = str(url)+"Saad-Lat Alarm", 
                        alarm_description = "SaadLat Alarm for"+ str(url), 
                        namespace = webcheck.URL_NAMESPACE,
                        metricname = webcheck.METRIC_NAME_LAT,
                        dimensions = Dimensions, threshold = webcheck.THRESHOLD_LAT,
                        sns_topic_arn = os.environ['topic_arn'], period = webcheck.sec_lim
            
        )
        
        cw.create_alarm(name = str(url)+"Saad-Avail Alarm", 
                        alarm_description = "Saad Availability Alarm for"+ str(url), 
                        namespace = webcheck.URL_NAMESPACE,
                        metricname = webcheck.METRIC_NAME_AVAIL,
                        dimensions = Dimensions, threshold = webcheck.THRESHOLD_AVAIL,
                        sns_topic_arn = os.environ['topic_arn'], period = webcheck.sec_lim
            
        )

        lst.update({'Url Name': url, 'availbility': avail, 'latency': latency})
        dim_values.append(lst)
    return values, dim_values
    

'''Get Availability Function '''

def get_availability(url):                      # To get availability of the urls, 1 shows availability and zero show not
    http = urllib3.PoolManager()                # creating a PoolManager instance for sending requests
    response = http.request("Get", url)         # sending a request and getting response
    if response.status == 200:
        return 1.0
    else:
        return 0.0

''' Get Latency Function'''

def get_latency(url):                        # To get latency of the urls
    http = urllib3.PoolManager()
    startTime = datetime.datetime.now()
    response = http.request("Get", url)
    endTime = datetime.datetime.now()        # check time after getting the website contents
    delta = endTime - startTime

    latencySec = round(delta.microseconds * .000001, 6)
    return latencySec