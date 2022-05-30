from aws_cdk import (
    # Duration,
    Stage,

)
import aws_cdk as cdk
from constructs import Construct

from sprint5_saad.sprint5_saad_stack import Sprint5SaadStack

class Sprint5SaadInfraStage(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        stage = Sprint5SaadStack(self, "Sprint5SaadStack")