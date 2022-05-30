import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint5_saad.sprint5_saad_stack import Sprint5SaadStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint5_saad/sprint5_saad_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Sprint5SaadStack(app, "sprint5-saad")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
