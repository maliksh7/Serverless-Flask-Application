import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint6_saad.sprint6_saad_stack import Sprint6SaadStack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint6_saad/sprint6_saad_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Sprint6SaadStack(app, "sprint6-saad")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
