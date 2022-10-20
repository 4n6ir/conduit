#!/usr/bin/env python3
import os

import aws_cdk as cdk

from conduit.conduit_stack import ConduitStack

app = cdk.App()

ConduitStack(
    app, 'ConduitStack',
    env = cdk.Environment(
        account = os.getenv('CDK_DEFAULT_ACCOUNT'),
        region = os.getenv('CDK_DEFAULT_REGION')
    ),
    synthesizer = cdk.DefaultStackSynthesizer(
        qualifier = '4n6ir'
    )
)

cdk.Tags.of(app).add('Alias','Pipeline')
cdk.Tags.of(app).add('GitHub','https://github.com/jblukach/conduit.git')

app.synth()
