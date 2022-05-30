from aws_cdk import (
    # Duration,
    Stack,
    pipelines,
    aws_codepipeline_actions as cp_actions_,
    SecretValue,
    aws_iam as iam,
    aws_codebuild as aws_cb_,
    # aws_sqs as sqs,
)

import aws_cdk as cdk
from constructs import Construct

from sprint5_saad.sprint5_saad_infra_stage import Sprint5SaadInfraStage

class Sprint5SaadPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        # defining pipeline riles
        pipeline_roles = self.create_role()        
    
        
        # source the pipeline
        source = self.github_source("saad2022skipq/Voyager", "main", "Saad-oauth-token")

                                                
        # Creates build step for synth 
        
        commands=["cd SaadHassan/Sprint5_Saad/", "pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"]
        primary_output_directory = "SaadHassan/Sprint5_Saad/cdk.out"
        
        synth = self.build_step("Synth", source, commands, primary_output_directory, pipeline_roles)


        # create the pipeline
        pipeline = self.create_pipeline("SaadPipeline", synth)
        
        # deploy the pipeline (production stage)
        
        # unit tests the resources before deploying

        commands=[
            "cd SaadHassan/Sprint4_Saad/",
            "ls",
            # "npm install -g aws-cdk",
            "pip install -r requirements.txt",
            "pip install -r requirements-dev.txt",
            "pytest --version",
            "pytest" ]
            
        unit_test = self.shell_step("Unit Test", commands)
        
        

        #docker test for the pipeline as post beta stage
        postbetastage = aws_cb_.BuildSpec.from_object(
                    {
                        "version": 0.2,
                        "phase": {
                            "install": {
                                "commands": [
                                                "nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://127.0.0.1:2375 --storage-driver=overlay2 &",
                                                "timeout 15 sh -c \"until docker info; do echo .; sleep 1; done\""
                                            ]
                                        },
                            "pre_build":{
                                "commands":[   
                                                "ls && cd sprint5_saad/pyrest" ,

                                                "docker build -t api-test-saad ."
                                            ]    
                                        },
                            "build":{
                                "commands": [
                                        "docker images",
                                        "docker run api-test-saad https://o1jhlqhjn2.execute-api.us-west-1.amazonaws.com api_test.yml"
                                    ]                                
                                }            
                            }    
                    }    

            )
            
        pyrrest_test = pipelines.CodeBuildStep("Saad-Pyresttest" , commands = [] ,
                        build_environment = aws_cb_.BuildEnvironment(
                                        build_image = aws_cb_.LinuxBuildImage.from_asset(self , "SaadPyrestImage" , directory = "./pyrest").from_docker_registry(name='docker:dind'),
                                        privileged = True), 
                        partial_build_spec = postbetastage)




        # instantiate beta-stage
        beta = Sprint5SaadInfraStage(self, "Saad-beta-stage")
        
        # add beta-stage to pipeline and before deployment run unit tests
        pipeline.add_stage(beta, pre = [unit_test], post=[pyrrest_test])
        
        # instantiate beta-stage
        prod = Sprint5SaadInfraStage(self, "Saad-prod-stage")
        
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
        

    # --------------------------------------------------------------------------    

        
        
    def shell_step(self, id, commands):
        
        '''
        Creates a shell step on the given commands
        
            Parameters:
                    id (str)        : id of shell step
                    command (list)  : list with all tthe commands
            
            Returns:
                    run the shell commands on the pre defined source
        '''
        
        return pipelines.ShellStep(id, commands = commands)
    
    
    def create_pipeline(self, id, synth):
        
        '''
        Creates an AWS Pipeline
        
            Parameters:
                    id (str)    : id of Pipeline
                    synth       : shell script to synthesize 
                    
            Returns:
                    creates a pipeline on AWS CodePipeline
        '''
        
        return pipelines.CodePipeline(self, id, synth = synth)
    
    
    def build_step(self, id, input, commands, primary_output_directory, role):
        
        '''
        Creates a build step with the given commands on the given source
        
            Parameters:
                    id (str)                    : id of build step
                    input                       : source on which it build the commands
                    commands (list)             : list of the commands
                    primary_output_directory    : directory where you wants to store the output
                    role                        : roles given to the build step
                    
            Returns:
                    run the build step commands on the given resource and store its output to a specific directory
        '''
        
        return  pipelines.CodeBuildStep(id, input = input, 
                                    commands = commands,
                                    primary_output_directory = primary_output_directory,
                                    role = role)
    
    
    def github_source(self, repo_string, branch, authentication_token):
        
        '''
        Creates a GitHub Source
        
            Parameters:
                    repo_string (str)               : name of the repo with id
                    branch (str)                    : name of the branch
                    authentication_token (str)      : access key of github that you store in AWS Secret Manager
                    
            Returns:
                    Github source
        '''
        
        return pipelines.CodePipelineSource.git_hub(repo_string = repo_string, 
                                                    branch = branch,
                                                    authentication = cdk.SecretValue.secrets_manager(authentication_token),
                                                    trigger = cp_actions_.GitHubTrigger.POLL)
        
   