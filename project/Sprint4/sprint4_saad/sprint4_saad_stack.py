from aws_cdk import (
    # Duration,
    Stage,
    Stack,
    aws_lambda as lambda_,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    RemovalPolicy, 
    Duration,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_sns_subscriptions as sns_subs_,
    aws_cloudwatch_actions as cw_actions,
    aws_iam as iam_,
    aws_dynamodb as dydb,
    aws_cloudwatch as cloudwatch,
    aws_dynamodb as dydb,
    aws_sns as sns_,
    aws_apigateway as apigw
)
import aws_cdk as cdk
import resources
from constructs import Construct
from resources import webcheck
from resources import webLoadData 
# import webLoadData 
from decimal import Decimal
import os, json


class Sprint4SaadStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        

        ''' ----------------------------- Logs Alarms data to Dynamodb table ----------------------------------- '''
        
        
        dynamo_db = self.create_table("Saad_table", "Timestamp","Subject")
        tableName = dynamo_db.table_name
        
        role = self.lambda_role()  # Saving roles for lambda in iam_role


        dynamodb_lambda = self.create_lambda("DynamoLambda", "./resources", "dynamoDB.lambda_handler", role)   #dynamo lambda for writing alarm logs to table

        dynamo_db.grant_full_access(dynamodb_lambda)
        
        
        ''' <---------------------------------------------------------------------------------------------------> '''





        ''' -------------------------------------- Web Health Lambda --------------------------------------------- '''
        
        WHLambda = self.create_lambda("WebHealthLambda", "./resources", "WebHealthLambda.lambda_handler", role )     # creation of lambda function with role and removal policy
        WHLambda.apply_removal_policy(RemovalPolicy.DESTROY)
        
        
        lambda_schedule = events_.Schedule.rate(Duration.minutes(1))   # invokes lambda periodically after every 1 minute
        lambda_target = targets_.LambdaFunction(handler=WHLambda)
        
        
        # Define EventBridge Rule in the stack --> bind source event with a target lambda function
        rule = events_.Rule(self, 
            "webHealth_Invocation_Rule", 
            description = "Periodic Lambda",
            enabled = True,
            schedule = lambda_schedule,
            targets = [lambda_target])     
            
        
        ''' <------------------------------------------------------------------------------------------------------> '''
            
            
            
            
            
        
        ''' -------------------------------------------- S3 Bucket -------------------------------------------------- '''    
        
        
        bkt = s3.Bucket(self, "Saad Voyager Bucket",
                        removal_policy = RemovalPolicy.DESTROY, 
                        auto_delete_objects = True, public_read_access = True)            # creating S3 bucket with removal policy 
                        
        
        s3deploy.BucketDeployment(self, "SkipQVoyager", 
                                  sources = [ s3deploy.Source.asset("./resources", exclude = ["*", "!webcheck.py"] ) ],
                                  destination_bucket = bkt )                       # initializing S3 bucket with file having web URLs
        
        
        # getting the bucket name
        bucketName = bkt.bucket_name
        
        

        ''' <---------------------------------------------------------------------------------------------------------> '''
        
        

        ''' ------------------------------------- Environment variables for Lambda ------------------------------------- '''

        # WHLambda.add_environment('bucket', bucketName)
        dynamodb_lambda.add_environment('tableName', tableName)

        my_topic = sns_.Topic(self, "SaadHassanTopic")                     # creating an sns topic and then adding an email subscription to the sns topic
        my_topicARN = my_topic.topic_arn # will senf this topic as environment variable to alarm
        
        my_topic.add_subscription(sns_subs_.EmailSubscription(webcheck.email))
        
        # linking an sns topic to lambda subscription
        my_topic.add_subscription(sns_subs_.LambdaSubscription(fn=dynamodb_lambda))
             



        ''' ------------------------------------------- Web Crawler Table ---------------------------------------------- '''
        
        # instantite the table and lambda to read json file from S3 bucket and store it to DynamoDB table
        webCrawler = self.create_table('Saad_webCrawler', 'id_', 'url')
        bktToDBHandler = self.create_lambda('Saad-Bucket-To-table', './resources', 's3_to_dynamoTable.bucket_to_dbHandler',role)
        bktToDBHandler.apply_removal_policy(RemovalPolicy.DESTROY)
        webCrawler.grant_full_access(bktToDBHandler)
        
        # add environment variables for S3 Bucket and table
        bktToDBHandler.add_environment('bucketName', bucketName)
        bktToDBHandler.add_environment('S3Totable', webCrawler.table_name)
        WHLambda.add_environment('bucketName', bucketName)
        WHLambda.add_environment('S3Totable', webCrawler.table_name)
        WHLambda.add_environment('topic_arn', my_topicARN)
        

        ''' ------------------------------------------------------------------------------------------------------------- '''





        ''' ------------------------------------------- Web Crawler API ------------------------------------------------- '''        
        
        # instantiating API lambda and giving it environent variables to access Bucket and DynamoDB table
        ApiHandler = self.create_lambda("SaadApiHandler", "./resources", "api_LambdaHandler.api_Handler", role)  
        ApiHandler.apply_removal_policy(RemovalPolicy.DESTROY)
        ApiHandler.add_environment('bucketName', bucketName)
        ApiHandler.add_environment('S3Totable', webCrawler.table_name)
        webCrawler.grant_full_access(ApiHandler)


        # instantiating API Gateway
        self.create_api('Saad-CRUD-Api', ApiHandler)
        
        
        
        ''' --------------------------------------------------------------------------------------------------------------- '''


    def alarm_metric_gen(self, my_topic):

        """ created access to urls, for each and every (availability and latency metrics), also creating respective alarms as well """  
        
        for url in webcheck.URLS_TO_MONITOR:                    
            dimension =  {'URL' : url} 
            
            # create cloudwatch metric for availability
            availability_metric = cloudwatch.Metric(metric_name=webcheck.METRIC_NAME_AVAIL, 
                                                    namespace= webcheck.URL_NAMESPACE, 
                                                    dimensions_map= dimension, 
                                                    period=Duration.minutes(1), 
                                                    )
            
            # create cloudwatch metric for latency
            latency_metric = cloudwatch.Metric(metric_name=webcheck.METRIC_NAME_LAT, 
                                              namespace= webcheck.URL_NAMESPACE, 
                                              dimensions_map= dimension, 
                                              period=Duration.minutes(1))
            
          
            # create an alarm for latency

            latency_alarm = cloudwatch.Alarm(self,
                                             id='saad_latency_alarm_' + "-" + url,
                                             metric=latency_metric,
                                             comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,                                              
                                             datapoints_to_alarm = 1,
                                             evaluation_periods = 1,
                                             threshold=webcheck.THRESHOLD_LAT
                                              )

            # setting an alarm for availability

            avail_alarm = cloudwatch.Alarm(self,
                                          id='saad_availability_alarm_' + "-" + url,
                                          metric = availability_metric,
                                          comparison_operator = cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
                                          datapoints_to_alarm = 1,
                                          evaluation_periods = 1,
                                          threshold=webcheck.THRESHOLD_AVAIL,
                                            )
                                            
            # linking sns and sns subscription to alarms for latency and availability of web resources
            avail_alarm.add_alarm_action(cw_actions.SnsAction(my_topic))
            latency_alarm.add_alarm_action(cw_actions.SnsAction(my_topic))
    
    
        
    def create_api(self,id_=None, handler_=None):
        
                
        """ 
        
            Description: Creates the lambda backed api to perform CRUD operations
            
            @param: self: scope(constructor)
            
            @param: idd (str): id for the api function,
      
            return: it returns the lambda backed api            
        
        """
        
        """
                        # creating a lambda-backed API Gateway
                        api = apigw.LambdaRestApi(self, id = id_, 
                                                    handler=handler_, 
                                                    proxy=False)
                
                        
                
                        # adding resource <health> and methods for it
                        health = api.root.add_resource("health")
                        health.add_cors_preflight(
                            allow_origins = apigw.Cors.ALL_ORIGINS,
                            )
                        health.add_method("GET", apigw.LambdaIntegration(handler_)) # GET /items
                
                        
                        # adding resource <url> and methods for it
                        url = api.root.add_resource("url")
                        url.add_cors_preflight(
                            allow_origins = apigw.Cors.ALL_ORIGINS,
                            )
                        url.add_method("GET", apigw.LambdaIntegration(handler_)) # GET /items
                        url.add_method("PUT", apigw.LambdaIntegration(handler_))
                        url.add_method("PATCH", apigw.LambdaIntegration(handler_))
                        url.add_method("DELETE", apigw.LambdaIntegration(handler_))
                
                        
                        return api
                        
        """
        
        api = apigw.LambdaRestApi(self, id = id_, handler=handler_)

        # adding resource <health> and methods for it
        health = api.root.add_resource("health")
        health.add_method("GET") # GET /items

        # adding resource <urls> and methods for it
        url = api.root.add_resource("url")
        url.add_method("GET")       # GET /url
        url.add_method("PUT")      # PUT /url
        url.add_method("PATCH")     # UPDATE /url
        url.add_method("DELETE")    # DELETE /url
        
        # returns the api
        return api
        
    def create_lambda(self, id_, asset, handler, role=None, timeout=Duration.seconds(60)):
        
        """
            Creates the lambda function
            
            @param: self: scope(constructor)
            
            @param: idd (str): id for the lambda function
            
            @param: asset (str): asset folder where the py file is located
            
            @param: handler (str): lambda handler function name in the py File (e.g. filename.functionName)
        
        """
        
        return lambda_.Function(self, id_,
            runtime= lambda_.Runtime.PYTHON_3_8,
            timeout= timeout,
            handler= handler,
            code= lambda_.Code.from_asset(asset),
            role=role
            )

    def lambda_role(self, id=None, assumed_by=None, managed_policies=None):  # creating a function for defining a lambda role
    
    
        '''
            
            AWS service principals
            
            A service principal is an identifier for a service. 
            IAM roles that can be assumed by an AWS service are called service roles. 
            Service roles must include a trust policy. 
            Trust policies are resource-based policies attached to a role that defines 
            which principals can assume the role.
            
        '''
    
        lambda_role = iam_.Role(self, "Role",
                               assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
                               managed_policies=[
                                                iam_.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                                                iam_.ManagedPolicy.from_aws_managed_policy_name(
                                                     'AmazonDynamoDBFullAccess'),
                                                iam_.ManagedPolicy.from_aws_managed_policy_name(
                                                     'service-role/AWSLambdaBasicExecutionRole'),
                                                iam_.ManagedPolicy.from_aws_managed_policy_name(
                                                     'AWSLambdaInvocation-DynamoDB'),
                                                iam_.ManagedPolicy.from_aws_managed_policy_name(
                                                     'AmazonAPIGatewayInvokeFullAccess'),
                                                iam_.ManagedPolicy.from_aws_managed_policy_name(
                                                     'AmazonAPIGatewayAdministrator')
                                                     
                                                ]
                                                  )
        return lambda_role


    # creating dynamo table
    def create_table(self, id,  partition_key=None, sort_key=None):
        
                
        """ 
        
            Description: Creates the table for dynamodb_lambda
            
            @param: self: scope(constructor)
            
            @param: idd (str): id for the table function,
      
            return: it returns dynamo_db table            
        
        """
        
        dynamo_table = dydb.Table(self, id,
            partition_key= dydb.Attribute(name=partition_key, type=dydb.AttributeType.STRING),
            sort_key= dydb.Attribute(name=sort_key, type=dydb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY)
            
        return dynamo_table
 
