import boto3
import json
import os
import zipfile
from subprocess import run

def handler(event, context):
    
    p = run( [ 'cdk', 'version' ], capture_output = True )
    print("AWS Cloud Development Kit (CDK)", p.stdout.decode())
    
    s3 = boto3.client('s3')
    s3.download_file(os.environ['BUCKET'], event['bundle'], '/tmp/'+event['bundle'])
    
    with zipfile.ZipFile('/tmp/'+event['bundle'], 'r') as z:
        z.extractall('/tmp')
    
    if event['type'] == 'deploy':

        p = run( [ 'cdk', 'deploy', '--all', '--require-approval', 'never' ], cwd = '/tmp/'+event['bundle'][:-4], capture_output = True)
        print(p.stdout.decode())

    if event['type'] == 'destroy':

        p = run( [ 'cdk', 'destroy', '--all', '--force' ], cwd = '/tmp/'+event['bundle'][:-4], capture_output = True)
        print(p.stdout.decode())

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }