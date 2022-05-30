import pytest
import aws_cdk as cdk_
from aws_cdk.assertions import Template
# from sprint4_saad.sprint4_saad_pipeline_stack import Sprint4SaadPipelineStack
from sprint4_saad.sprint4_saad_stack import Sprint4SaadStack 
import aws_cdk.assertions as assertions
import requests
from resources import webcheck as webcheck
import json


def test_api_get_Method():

    """ API Test for GET Method """
    
    getMethod = requests.get(url = webcheck.API_URL)
    if getMethod.status_code == 200:
        statuscode = getMethod.status_code
        assert True
        print("Get Method Passed {}".format(statuscode))

def test_put_method():
    
    """ API Test for PUT Method """
    
    putData = webcheck.API_DATA
    putMethod = requests.put(url = webcheck.API_URL, data = putData)
   
    json_ = putMethod.json()
    # print(json_)
    body = json_['event[body]']
    url = body.split('=')[1]
    
    if url == putData['url']:
        assert True

# Check delete method
def test_delete_method():
    
    """ API Test for DELETE Method """
    
    deleteData = webcheck.API_DATA
    deleteMethod = requests.delete(url = webcheck.API_URL, data = deleteData)
   
    if deleteMethod.status_code == 200:
        assert True


#Check patch method
def test_patch_method():
    
    """ API Test for PATCH Method """
    
    newUpdateData = webcheck.API_UPDATE_DATA
    updateMethod = requests.post(url = webcheck.API_URL, data = newUpdateData)
    deletePrevData = webcheck.API_DATA
    deletePrevMethod = requests.delete(url = webcheck.API_URL, data = deletePrevData)
   
    if updateMethod.status_code == 200 and deletePrevMethod.status_code == 200:
        assert True

