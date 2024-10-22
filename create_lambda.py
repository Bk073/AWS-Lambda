import boto3
import botocore
import json
import io
import zipfile

def create_iam_role():
    iam_client = boto3.client('iam')
    role_name = 'my-lambda-execution-role'
    trust_policy = {
        "Version":"2012-10-17",
        "Statement":[
            {
                "Effect":"Allow",
                "Principal":{
                    "Service":"lambda.amazonaws.com"
                },
                "Action":[
                    "iam:Get*",
                    "iam:List*"
                    "iam:Create*"
                ]
            }
        ]
    }
    response = iam_client.create_role(
        RoleName = role_name,
        AssumeRolePolicyDocument = json.dumps(trust_policy),
        Description="IAM role for Lambda execution",
    )
    policy_arn = 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
    iam_client.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn
    )


def create_function(lambda_code):
    lambda_client = boto3.client('lambda', region_name='us-east-1')

    response = lambda_client.create_function(
        FunctionName = 'lambda_using_sdk',
        Runtime='python3.8',
        Role='arn:aws:iam::568905016485:role/my-lambda-execution-role',
        Handler='lambda_function.lambda_handler',
        Code={
            'ZipFile':lambda_code,
        },
        Description="My Lambda function created via Boto3",
        Timeout=60,
        MemorySize=128,
        Publish=True,
    )

def create_zip():
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zipped_file:
        zipped_file.writestr('lambda_hello.py', open('lambda_hello.py').read())
    buffer.seek(0)
    return buffer.read()

def invoke_lambda():
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    response = lambda_client.invoke(
        FunctionName='lambda_using_sdk',
        InvocationType='RequestResponse',
        Payload=json.dumps({"key":"value"})
    )
    return response

if __name__ == '__main__':
    lambda_code = create_zip()
    create_function(lambda_code)
    response = invoke_lambda()
    print(response["Payload"].read().decode('utf-8'))
