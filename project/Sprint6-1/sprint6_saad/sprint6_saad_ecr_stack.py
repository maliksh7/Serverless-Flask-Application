from aws_cdk import (
    # Duration,
    Stack,
    core,
    aws_ecr as ecr,
    aws_ecr_assets as ecra,
    cdk_ecr_deployment as ecrdeploy
    # aws_sqs as sqs,
)
from constructs import Construct

class Sprint6SaadECRStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

    # Create ECR
    def create_ecr_repository(self):
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecr/Repository.html
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
        
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecr_assets/DockerImageAsset.html
        image = ecra.DockerImageAsset(self, "Saad-flask-image",
            # The directory where the Dockerfile is stored.
            directory = './app'
            
        )
        
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_ecr_assests/README.html#publishing-images-to-ecr-repositories
        ecrdeploy.ECRDeployment(self, 'DeployDockerImage',
            src = ecrdeploy.DockerImageName(image.image_url),
            dest=ecrdeploy.DockerImageName(f"{self.ecr_repo.repository_url}:latest"),
            
        );
        