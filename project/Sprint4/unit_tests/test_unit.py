import pytest
import aws_cdk as cdk_
from aws_cdk.assertions import Template
# from sprint3_saad.sprint3_saad_pipeline_stack import Sprint3SaadPipelineStack
from sprint4_saad.sprint4_saad_stack import Sprint4SaadStack 
import aws_cdk.assertions as assertions
import requests
from resources import webcheck as webcheck


@pytest.fixture
def test_unit():
   app = cdk_.App()
   stack = Sprint4SaadStack(app, "sprint4-saad")
   template = assertions.Template.from_stack(stack)
   return template 
   
   
def test_lambda(test_unit):   
   test_unit.resource_count_is("AWS::Lambda::Function", 6) 

def test_dynamo(test_unit):
   test_unit.resource_count_is("AWS::DynamoDB::Table", 2)
   
def test_bucket(test_unit):   
   test_unit.resource_count_is("AWS::S3::Bucket", 1)

# # def test_api(test_unit):
# #    """
   
# #     "SaadCRUDApiFE7E5D73": {
# #       "Type": "AWS::ApiGateway::RestApi",
# #       "Properties": {
# #        "Name": "Saad-CRUD-Api"
# #       },
# #       "Metadata": {
# #        "aws:cdk:path": "Sprint4SaadStack/Saad-CRUD-Api/Resource"
# #       }
# #     },
   
   
# #    """
# #    test_unit.resource_count_is


# #
# '''

#    after invoking url, parse the invoked url and check if it matches the url to process
#    if it does, assert True
#    ^^ these are for unit tests
   
#    for Integration tests, invoke url and check from database whether the invocation executed or not, if it does, assert True
   
   
#    ---------------------------------------------------------
#    Example for unit test
#    def test_api_put_method():
       
       
#    #     r = requests.put(cts.url, data=cts.payload)
#    #     a = r.json()
#    #     b = a['event[body]']
#    #     c = b.split('=')[1]
   
#    #     if c == cts.payload["url"]:
#    #        c == www.skipq.org == cts.payload
#    #     #     print("url has been added to the table")
#    #         assert True
#    ___________________________________________
#    example for integration test
   
#    # def test_delete_action():
   
#    #     api_test = requests.delete(cts.url, data=cts.payload)
#    #     response = table.get_item(
#    #                                 Key={
#    #                                 "url": cts.payload["url"],
#    #                             })
#    #     a = api_test.json() #converts api_test to json object
#    #     r = a['event[body]'] #extracting event body
#    #     c = r.split('=')[1] #parsing to recieve url
#    #     response = table.get_item( Key={"url": cts.payload["url"],}) #search table
#    #     if "Item" not in response:
#    #         assert True
#    #         cts.url = api_url
#    #         cts.payload = dummy url-> google.com

#    # https://docs.python-requests.org/en/latest/user/quickstart/#make-a-request

#    # r = requests.get('https://api.github.com/events')
   
#    # Now, we have a Response object called r. We can get all the information we need from this object.

#    # Requests’ simple API means that all forms of HTTP request are as obvious. For example, this is how you make an HTTP POST request:


# '''