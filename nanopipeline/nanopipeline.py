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

    os.system('cd /tmp | ls -lh')

    if event['type'] == 'deploy':
        
        command = 'cd /tmp/'+event['bundle']+' && cdk deploy --all --require-approval never' 
        p = run( [ command ], capture_output = True)
        print(p.stdout.decode())

    if event['type'] == 'destroy':
    
        command = 'cd /tmp/'+event['bundle']+' && cdk destroy --all --force'
        p = run( [ command ], capture_output = True)
        print(p.stdout.decode())

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }