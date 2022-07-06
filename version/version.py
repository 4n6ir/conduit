import boto3
import feedparser
import json
import os
from github import Github

def handler(event, context):

    try:
        poll_response = feedparser.parse('https://github.com/aws/aws-cdk/releases.atom')
    except:
        raise ValueError('RSS/Atom Feed Failure')  

    ssm_client = boto3.client('ssm')
    
    response = ssm_client.get_parameter(
        Name = os.environ['VERSIONS']
    )
    
    prevtoken = response['Parameter']['Value']

    if poll_response.entries[0].title != prevtoken:

        if poll_response.entries[0].title[0:2] == 'v2':

            f = open('/tmp/Dockerfile', 'w')
            f.write('# CDK '+poll_response.entries[0].title+'\n')
            f.write('FROM public.ecr.aws/lambda/python:latest\n')
            f.write('RUN yum -y update\n')
            f.write('RUN curl -sL https://rpm.nodesource.com/setup_16.x | bash -\n')
            f.write('RUN yum list available nodejs\n')
            f.write('RUN yum install -y nodejs\n')
            f.write('RUN npm install -g aws-cdk@latest\n')
            f.write('RUN yum clean all\n')
            f.write('COPY nanopipeline.py requirements.txt ./\n')
            f.write('RUN pip --no-cache-dir install -r requirements.txt --upgrade\n')
            f.write('CMD ["nanopipeline.handler"]\n')
            f.close()

            with open('/tmp/Dockerfile', 'r') as f:
                data = f.read()
            f.close()
            
            secret_client = boto3.client('secretsmanager')

            response = secret_client.get_secret_value(
                SecretId = 'github-token'
            )

            g = Github(response['SecretString'])

            repo = g.get_repo('jblukach/conduit')

            contents = repo.get_contents('nanopipeline/Dockerfile')

            repo.update_file(contents.path, poll_response.entries[0].title, data, contents.sha)

            response = ssm_client.put_parameter(
                Name = os.environ['VERSIONS'],
                Value = poll_response.entries[0].title,
                Type = 'String',
                Overwrite = True
            )

    return {
        'statusCode': 200,
        'body': json.dumps('Conduit Version')
    }