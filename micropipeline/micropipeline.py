import boto3
import json
import os
import time
import zipfile
from subprocess import run

def lambdaHandler(event, context):
    
    p = run( [ 'cdk', 'version' ], capture_output = True )
    print("AWS Cloud Development Kit (CDK)", p.stdout.decode())
    
    os.system('df -h')

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }