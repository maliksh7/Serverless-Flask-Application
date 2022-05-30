from aws_cdk import (
    # Duration,
    Stack,
    # core,
    aws_ecr as ecr,
    aws_ecr_assets as ecra,
    # cdk_ecr_deployment as ecrdeploy
    # aws_sqs as sqs,
)
from constructs import Construct

import cdk_ecr_deployment as ecrdeploy 

class Sprint6SaadECRStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        self.ecr_repository=self.create_ecr_repositry()
        self.create_and_deploy_image()
        
    # Create ECR
    def create_ecr_repositry(self):
        
        '''
           
           Docs:          https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecr/Repository.html
           Description:   This function will create a repository that's Elastic Container Repository(ECR).
           @param:        self(constructor)
           Returns:       returns a repository
           
        '''
        
        return ecr.Repository(self, "Saad_ecr_repo",
            # Name for this repository. Default: Automatically generated name.
            # repository_name = "ecr_repo"
            # Image scanning helps in identifying software vulnerabilities in your container images.
            # Ensures that each new image pushed to the repository is scanned
            image_scan_on_push=True,
            # The tag mutability setting for the repository. default MUTABLE
            # all image tags within the repository will be immutable which will prevent them from being overwritten. 
            image_tag_mutability= ecr.TagMutability.IMMUTABLE,
            # Lifecycle policies help which managing the lifecycle of the images in your repositories.
            # You define rules that result in the cleaning up of unused images.
            lifecycle_rules = [
                # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecr/LifecycleRule.html
                ecr.LifecycleRule(
                    description="Only retain 200 images",
                    max_image_count=200,      # The maximum number of images to retain
                    rule_priority=1,
                    
                    )
                ]
            )
            
    # Create Image
    def create_and_deploy_image(self):
        
        '''
           
           Description:   This function will create a docker image so that i can distribute it 
                          and can be used by my Flask App. 
           @param:        self(constructor)
           Returns:       creates and deploys a docker image
           
        '''
        
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecr_assets/DockerImageAsset.html
        # DockerImageAsset is fun of cdk api to build a image
        image = ecra.DockerImageAsset(self, "Saad-flask-image",
            # The directory where the Dockerfile is stored.
            directory = './app'
            
        )
        
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecr_assests/README.html#publishing-images-to-ecr-repositories
        # upload an image to ECR repo
        ecrdeploy.ECRDeployment(self, 'DeployDockerImage',
            src = ecrdeploy.DockerImageName(image.image_uri),
            dest=ecrdeploy.DockerImageName(f"{self.ecr_repository.repository_uri}:latest"),
            
        );
        