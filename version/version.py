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

            f = open('/tmp/'+poll_response.entries[0].title, 'w') 
            f.write(poll_response.entries[0].link)
            f.close()

            with open('/tmp/'+poll_response.entries[0].title, 'rb') as binary_file:
                binary_data = binary_file.read()

            secret_client = boto3.client('secretsmanager')

            response = secret_client.get_secret_value(
                SecretId = 'github-token'
            )

            g = Github(response['SecretString'])

            repo = g.get_repo('jblukach/conduit')

            repo.create_file('status/'+poll_response.entries[0].title, poll_response.entries[0].title, binary_data, branch='main')

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