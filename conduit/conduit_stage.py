import aws_cdk as cdk

from constructs import Construct

from conduit.conduit_app import ConduitApp

class ConduitStage(cdk.Stage):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        appStack = ConduitApp(
            self, 'app',
            synthesizer = cdk.DefaultStackSynthesizer(
                qualifier = '4n6ir'
            )
        )
