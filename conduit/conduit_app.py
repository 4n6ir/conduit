from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_iam as _iam,
    aws_lambda as _lambda,
    aws_logs as _logs,
    aws_s3 as _s3,
    aws_ssm as _ssm
)

from constructs import Construct

class ConduitApp(Stack):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        account = Stack.of(self).account
        region = Stack.of(self).region
        micro_pipeline = 'conduit-micropipeline-'+account+'-'+region

        bucket = _s3.Bucket(
            self, 'bucket',
            bucket_name = micro_pipeline,
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            versioned = True,
        )

        role = _iam.Role(
            self, 'role', 
            assumed_by = _iam.ServicePrincipal(
                'lambda.amazonaws.com'
            )
        )

        role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaBasicExecutionRole'
            )
        )

        role.add_managed_policy(
            _iam.ManagedPolicy.from_aws_managed_policy_name(
                'service-role/AWSLambdaVPCAccessExecutionRole'
            )
        )

        role.add_to_policy(
            _iam.PolicyStatement(
                actions = [
                    's3:GetObject',
                    'sts:AssumeRole'
                ],
                resources = ['*']
            )
        )

        micropipeline = _lambda.DockerImageFunction(
            self, 'micropipeline',
            function_name = micro_pipeline,
            code = _lambda.DockerImageCode.from_image_asset('micropipeline'),
            timeout = Duration.seconds(900),
            environment = dict(
                BUCKET = bucket.bucket_name
            ),
            memory_size = 2048,
            role = role,
            vpc = vpc
        )

        micropipelinelogs = _logs.LogGroup(
            self, 'micropipelinelogs',
            log_group_name = '/aws/lambda/'+micropipeline.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        micropipelinemonitor = _ssm.StringParameter(
            self, 'micropipelinemonitor',
            description = 'Conduit Micropipeline',
            parameter_name = '/conduit/micropipeline',
            string_value = '/aws/lambda/'+micropipeline.function_name,
            tier = _ssm.ParameterTier.STANDARD,
        )
