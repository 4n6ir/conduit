from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_events as _events,
    aws_events_targets as _targets,
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
        nano_pipeline = 'conduit-nanopipeline-'+account+'-'+region

### S3 BUCKETS ###

        nanobucket = _s3.Bucket(
            self, 'nanobucket',
            bucket_name = nano_pipeline,
            encryption = _s3.BucketEncryption.S3_MANAGED,
            block_public_access = _s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy = RemovalPolicy.DESTROY,
            auto_delete_objects = True,
            versioned = True,
        )

### IAM ROLE ###

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
                    'secretsmanager:GetSecretValue',
                    'ssm:GetParameter',
                    'ssm:PutParameter',
                    'sts:AssumeRole'
                ],
                resources = ['*']
            )
        )

### NANOPIPLINE ###

        nanopipeline = _lambda.DockerImageFunction(
            self, 'nanopipeline',
            function_name = nano_pipeline,
            code = _lambda.DockerImageCode.from_image_asset(
                'nanopipeline',
                build_args = {
                    'NOCACHE': '--no-cache'
                }
            ),
            timeout = Duration.seconds(900),
            environment = dict(
                BUCKET = nanobucket.bucket_name
            ),
            memory_size = 1048,
            role = role
        )

        nanopipelinelogs = _logs.LogGroup(
            self, 'nanopipelinelogs',
            log_group_name = '/aws/lambda/'+nanopipeline.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        nanopipelinemonitor = _ssm.StringParameter(
            self, 'nanopipelinemonitor',
            description = 'Conduit Nanopipeline',
            parameter_name = '/conduit/nanopipeline',
            string_value = '/aws/lambda/'+nanopipeline.function_name,
            tier = _ssm.ParameterTier.STANDARD,
        )

### VERSION UPDATE ###

        versions = _ssm.StringParameter(
            self, 'versions',
            description = 'Conduit Version',
            parameter_name = '/conduit/version',
            string_value = 'Empty',
            tier = _ssm.ParameterTier.STANDARD
        )

        version = _lambda.DockerImageFunction(
            self, 'version',
            code = _lambda.DockerImageCode.from_image_asset('version'),
            environment = dict(
                VERSIONS = versions.parameter_name
            ),
            timeout = Duration.seconds(900),
            memory_size = 512,
            role = role
        )

        versionlogs = _logs.LogGroup(
            self, 'versionlogs',
            log_group_name = '/aws/lambda/'+version.function_name,
            retention = _logs.RetentionDays.ONE_DAY,
            removal_policy = RemovalPolicy.DESTROY
        )

        versionmonitor = _ssm.StringParameter(
            self, 'versionmonitor',
            description = 'Conduit Version Monitor',
            parameter_name = '/conduit/monitor/version',
            string_value = '/aws/lambda/'+version.function_name,
            tier = _ssm.ParameterTier.STANDARD,
        )

        event = _events.Rule(
            self, 'event',
            schedule = _events.Schedule.cron(
                minute = '0',
                hour = '*',
                month = '*',
                week_day = '*',
                year = '*'
            )
        )
        event.add_target(
            _targets.LambdaFunction(version)
        )
