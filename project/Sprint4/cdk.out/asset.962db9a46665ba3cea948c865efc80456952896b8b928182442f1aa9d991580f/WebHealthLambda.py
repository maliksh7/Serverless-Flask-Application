import urllib3
import datetime
import os
import boto3  # python sdk
import sys  # importing access keys from a file

from cloudWatch import cloudWatch
# from webLoadData import webURLS as wl
# import webcheck
# wl.load_urls(webcheck.URLS_TO_MONITOR)

def lambda_handler(event, context):
    # downloading file from the created bucket using boto3 client
    s3 = boto3.client('s3')
    s3.download_file(os.environ['bucket'], 'webcheck.py', '/tmp/webcheck.py')

    # giving path of the imported file
    sys.path.insert(1, '/tmp')

    import webcheck
    
    # w_url = webURLS()
    cw = cloudWatch()
    # creating an object of class Cloudwatchputmetric()
    values = []
    for url in webcheck.URLS_TO_MONITOR:
        avail = get_availability(url)
        latency = get_latency(url)

        Dimensions = [                      #defining dimesions for our metrics
            {"Name": "URL", "Value": url},
        ]
        cw.put_data(webcheck.URL_NAMESPACE, webcheck.METRIC_NAME_AVAIL, Dimensions,
                    avail)  # data for availability metric

        cw.put_data(webcheck.URL_NAMESPACE, webcheck.METRIC_NAME_LAT, Dimensions,
                    latency)  # data for latency metric

        values.append({'website': url, 'availbility': avail, 'latency': latency})

    return values

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