from aws_cdk import (
    # Duration,
    Stage,

)
import aws_cdk as cdk
from constructs import Construct

from sprint4_saad.sprint4_saad_stack import Sprint4SaadStack

class Sprint4SaadInfraStage(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        stage = Sprint4SaadStack(self, "Sprint4SaadStack")