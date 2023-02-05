import aws_cdk as cdk

from aws_cdk import Aspects
from aws_cdk import Stack

from aws_cdk.pipelines import (
    CodePipeline,
    CodePipelineSource,
    ShellStep
)

import cdk_nag

from constructs import Construct

from conduit.conduit_stage import ConduitStage

class ConduitStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Aspects.of(self).add(
            cdk_nag.AwsSolutionsChecks(
                log_ignores = True,
                verbose = True
            )
        )

        cdk_nag.NagSuppressions.add_stack_suppressions(
            self, suppressions = [
                {'id': 'AwsSolutions-S1','reason': 'GitHub Issue'},
                {'id': 'AwsSolutions-IAM5','reason': 'GitHub Issue'},
                {'id': 'AwsSolutions-CB3','reason': 'GitHub Issue'},
                {'id': 'AwsSolutions-CB4','reason': 'GitHub Issue'}
            ]
        )

        account = Stack.of(self).account
        region = Stack.of(self).region

        pipeline = CodePipeline(
            self, 'pipeline', 
            synth = ShellStep(
                'Synth', 
                input = CodePipelineSource.git_hub(
                    'jblukach/conduit',
                    'main'
                ),
                commands = [
                    'npm install -g aws-cdk', 
                    'python -m pip install -r requirements.txt', 
                    'cdk synth'
                ]
            ),
            docker_enabled_for_synth = True
        )

        #pipeline.add_stage(
        #    ConduitStage(
        #        self, 'conduit',
        #        env = cdk.Environment(
        #            account = account,
        #            region = region
        #        )
        #    )
        #)

        #pipeline.build_pipeline()
