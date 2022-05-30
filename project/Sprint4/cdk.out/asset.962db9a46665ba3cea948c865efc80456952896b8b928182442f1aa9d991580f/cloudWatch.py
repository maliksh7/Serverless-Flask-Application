import boto3

'''CloudWatch Metrics Data'''
class cloudWatch:
    def __init__(self):
        self.client = boto3.client("cloudwatch")

    def put_data(self, nameSpace, MetricName, Dimensions, value):
        response = self.client.put_metric_data(
            Namespace=nameSpace,
            MetricData=[
                {
                    "MetricName": MetricName,
                    "Dimensions": Dimensions,
                    "Value": value
                }
            ]
        )