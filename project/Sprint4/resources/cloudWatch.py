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
        
    def create_alarm(self,name, alarm_description, metricname, namespace, dimensions, threshold, sns_topic_arn, period):
    
        return self.client.put_metric_alarm(
            AlarmName = name,
            AlarmDescription = alarm_description,
            ActionsEnabled=True,
            AlarmActions=[sns_topic_arn],
            MetricName = metricname,
            Namespace = namespace,  
            Statistic = 'Average', 
            Dimensions = dimensions,
            Period = period,         
            EvaluationPeriods = 1,  
            Threshold = threshold,  
            ComparisonOperator='GreaterThanOrEqualToThreshold',
            )