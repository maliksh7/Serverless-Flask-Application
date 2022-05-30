import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint4_saad.sprint4_saad_stack import Sprint4SaadStack
import requests as re
# example tests. To run these tests, uncomment this file along with the example
# resource in sprint4_saad/sprint4_saad_stack.py
# def test_sqs_queue_created():
#     app = core.App()
#     stack = Sprint4SaadStack(app, "sprint4-saad")
#     template = assertions.Template.from_stack(stack)

# #     template.has_resource_properties("AWS::SQS::Queue", {
# #         "VisibilityTimeout": 300
# #     })

# def test_api_get_Method():
   
#   """ API Test for GET Method """
   
#   getMethod = re.get(url = webcheck.API_URL)
#   if getMethod.status_code == 200:
#       statuscode = getMethod.status_code
#       assert True
#       print("Get Method Passed {}".format(statuscode))