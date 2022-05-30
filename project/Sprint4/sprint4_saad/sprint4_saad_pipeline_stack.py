from aws_cdk import (
    # Duration,
    Stack,
    pipelines,
    aws_codepipeline_actions as cp_actions_,
    SecretValue,
    aws_iam as iam
    # aws_sqs as sqs,
)

import aws_cdk as cdk
from constructs import Construct

from sprint4_saad.sprint4_saad_infra_stage import Sprint4SaadInfraStage

class Sprint4SaadPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
    
        
        # source the pipeline
        source = pipelines.CodePipelineSource.git_hub("saad2022skipq/Voyager", "main", 
                                                        authentication=SecretValue.secrets_manager("Saad-oauth-token"), 
                                                        trigger = cp_actions_.GitHubTrigger("POLL")
                                                        )
                                                        
        
        pipeline_roles = self.create_role()                                                
        
        # build the pipeline
        synth=pipelines.CodeBuildStep("Synth",
            input= source,
            commands=["cd SaadHassan/Sprint4_Saad/", "pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"],
            primary_output_directory = "SaadHassan/Sprint4_Saad/cdk.out",
            role=pipeline_roles
        )
        
        pipeline = pipelines.CodePipeline(self, "SaadPipeline", synth= synth )
        
        ## deploy the pipeline (production stage)
        
        # unit tests the resources before deploying
        
        unit_test =pipelines.ShellStep(
            "Unit Test",
            commands=[
                "cd SaadHassan/Sprint4_Saad/",
                "ls",
                # "npm install -g aws-cdk",
                "pip install -r requirements.txt",
                "pip install -r requirements-dev.txt",
                "pytest --version",
                "pytest" ]
        )
        
        # instantiate beta-stage
        
        beta = Sprint4SaadInfraStage(self, "Saad-beta-stage")
        
        # add beta-stage to pipeline and before deployment run unit tests
        
        pipeline.add_stage(beta, pre = [unit_test])
        
        # instantiate beta-stage
        
        prod = Sprint4SaadInfraStage(self, "Saad-prod-stage")
        
        # add beta-stage to pipeline
        
        pipeline.add_stage(prod, pre = [pipelines.ManualApprovalStep("saad_test-step")]) # added a manual approval step


    
    def create_role(self):  
            
        """
            Description: creating a function for defining a roles for pipeline
            
            Represents a principal that has multiple types of principals.
    
            A composite principal cannot have conditions. i.e. multiple 
            ServicePrincipals that form a composite principal 
            
            AWS service principals
            
            A service principal is an identifier for a service. 
            IAM roles that can be assumed by an AWS service are called service roles. 
            Service roles must include a trust policy. 
            Trust policies are resource-based policies attached to a role that defines 
            which principals can assume the role
            
            @param: self: scope(constructor)
            
            return: this function returns the roles for pipeline
        
        """
        role = iam.Role(self, "Pipeline-Role",
                      assumed_by=iam.CompositePrincipal(
                          iam.ServicePrincipal("lambda.amazonaws.com"),
                          iam.ServicePrincipal("sns.amazonaws.com"),
                          iam.ServicePrincipal("codebuild.amazonaws.com")),
                      managed_policies=
                      [
                        iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchFullAccess'),
                        iam.ManagedPolicy.from_aws_managed_policy_name('AmazonDynamoDBFullAccess'),
                        iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole'),
                        iam.ManagedPolicy.from_aws_managed_policy_name('AWSLambdaInvocation-DynamoDB'),
                        
                        iam.ManagedPolicy.from_aws_managed_policy_name("AwsCloudFormationFullAccess"),
                        iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMFullAccess"),
                        iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodePipeline_FullAccess"),
                        iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")                  
                        
                        ])
        return role