# Lambda

## Lambda execution environment lifecycle:

- https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html
- By default, each AWS account has a concurrency limit of 1,000 concurrent executions across all Lambda functions in a given region, This limit can be raised by requesting for AWS to increase the limit of the concurrent executions of your account.
- Lambda invokes function in execution environment which manages the resources required for the function
- When you create lambda, you specify memory, maximum execution time, etc and lambda uses this information to set up the execution environment
- The execution environment provides lifecycle support for the function's runtime and any external extensions
    - meaning the execution environment is responsible for:
        - Running the runtime for lambda function (such as python, node.js, etc)
        - Handling invocation of the function
        - Managing the function's lifecycle, including cold starts and warm invocations

        Cold Start:
            - When a lamnda function is invoked for the first time and new execution environment is created
        Warm Invocations:
            - Lambda attempts to reuse execution environments for subsequent invocations to reduce cold start latency as it skips initialization steps

        - Supporting external extensions that enhance or customize the behavior of the Lambda functions



## Lambda execution environment lifecycle:

INIT -> INVOKE -> INVOKE -> SHUTDOWN

## Concurrency in Lambda:
- concurrent executions = (invocations per second) x (average execution duration in seconds)
- AWS Lambda dynamically scales function execution in response to increased traffic, up to your concurrency limit.

# Invoking functions:
- Invoke lambda function based on an event that occurs elsewhere in the application
- Some services can invoke a Lambda function with each new event called trigger. 
- For stream and queue-based services, Lambda invokes the function with batches of records called **event source mapping**
- 

## Invocation type:
- https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html
- When you invoke a function, you can choose to invoke it synchronously or asynchronously. 
- Trigger based invocation:
    - some services(s3) can invoke a lambda function with each new event 
    - we have no control over the invocation type
- Event source mapping: 
    - for stream and queue-based services and invoke in batches of records
    - using Invoke API
- In Invoke API, Invocation type:
    - RequestResponse - synchronously
    - Event - acynchronously
    - DryRun 
- Invocation type parameter is used

### Synchronous invocation
- you wait for the function to process the event and return the response
- the connection is open until the function returns a response or time out
- **invoke** command in AWS CLI invokes function synchronously and returns a response

### Asynchronous invocation
- Lambda queues the event for processing and returns a response immediately
- Several services like S3, SNS, invoke functions asynchronously to process events
- For asynchronous invocation, Lambda places the event in a queue and returns a success response without additional information. A separate process reads events from the queue and sends them to your function.
- In CLI:
    - use **invocation-type=Event** in **invoke** command
- 
## Event Source Mappings:
- https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html
- An event source mapping is a Lambda resource that **reads items from stream and queue-based services ** and **invokes a function**
- Some services like S3, SNS, Amazon API Gateway can directly invoke Lambda functions using triggers.
    - Triggers are suitable for discrete events and real-time processing

- Event source mappings are Lambda resources designed for processing high-volume streaming data or messages from queues.
    - Processing records from a stream or queue in batches is more efficient than processing records individually.
- You can configure batching window(maximum amount of time to gather records into a single payload) and batch size
- By default, if your function returns an error, the event source mapping reprocesses the entire batch until the function succeeds, or the items in the batch expire
### Event source mapping API:
    - CreateEventSourceMapping
    - ListEventSourceMappings
    - GetEventSourceMapping
    - UpdateEventSourceMapping
    - DeleteEventSourceMapping


# Configuring Lambda functions:
## Deploying Lambda functions as .zip file archives
- Lambda supports two types of deployment packages:
    i. Container Images
    ii. .zip file archives

- **The workflow to create a function depends on the deployment package type**

## Memory:
- Lambda allocated CPU power in proportion to the amount of memory configured
- Configure memory between 128MB to 10,240 MB
- use **memory-size** parameters

### Determining appropriate memory setting:
- If a function is CPU, network or memory-bound, then increasing the memory setting can dramatically improve its performance.
- Use: 
    - https://github.com/alexcasalboni/aws-lambda-power-tuning 


## Lambda environment variables to configure values in code:
- An environment variable is a pair of strings that is stored in a function's version-specific configuration.
AWS SKDs(boto3) use:
- UpdataFunctionConfiguration
- GetFunctionConfiguration
- CreateFunction

## Attach Lambda function to VPC:
```import boto3

# Initialize boto3 client for Lambda
lambda_client = boto3.client('lambda')

# Parameters
function_name = 'your-lambda-function-name'
vpc_config = {
    'SubnetIds': [
        'subnet-xxxxxxxx',  # Add your subnet IDs
        'subnet-yyyyyyyy',
    ],
    'SecurityGroupIds': [
        'sg-xxxxxxxx',  # Add your security group IDs
    ]
}

# Update the Lambda function configuration to attach it to the VPC
response = lambda_client.update_function_configuration(
    FunctionName=function_name,
    VpcConfig=vpc_config
)

# Print the response
print(response)
```

## AWS lambda API references:
### Core lambda API operations:

1. Create Function
- Creates a new Lambda function with specified code, runtime, and execution role.
- Required parameters: FunctionName, Runtime, Role, Handler, Code

2. Invoke Function
- Triggers the function synchronously or asynchronously
- Parameters: FunctionName, InvocationType, Payload

3. Update Function Code
- Updates the deployment package of an existing function
- Parameters: FunctionName, ZipFile

4. Update Function Configuration
- Modifies settings such as memory, timeout or environment variables
- Parameters: FunctionName, MemorySize, Timeout, Environment

5. Delete Function
- Deletes a Lambda function
- Parameters: FunctionName

### Permissions & Access Control

1. Add Permissions
- Grants permission to another service to invoke your Lambda functions
- Parameters: FunctionName, Action, Principal, StatementID

2. Remove Permissions
- Removes permissions previously added to a function
- Parameters: FunctionName, StatementId


### Monitoring and Logs

1. Get Function Logs (via CloudWatch)
- Lambda functions automatically log to CloudWatch Logs

2. Get Function Information
- Retrieves metadata and code location of a Lambda function
- Parameter: FunctionName

3. List Functions
- Lists all Lambda functions in the account

