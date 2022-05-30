import aws_cdk as core
import aws_cdk.assertions as assertions

from sprint6_saad2.sprint6_saad2_stack import Sprint6Saad2Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint6_saad2/sprint6_saad2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Sprint6Saad2Stack(app, "sprint6-saad2")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
