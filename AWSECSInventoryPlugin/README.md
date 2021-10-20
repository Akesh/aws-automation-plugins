# Amazon ECS Inventory | Monitoring

## Pre-Requisites
If you are creating this stack from your local or from EC2 instance, provide necessary permissions on following services to succesfully create stack
- Cloudformation
- S3
- Lambda
- API gateway


## Capability
This automation intents to list all the ECS clusters and respective ECS services in a region along with health of each and individual service. Lambda function can be invoked with API Gateway URL `GET` and data will be published in a `HTML Table` on your browser. This report gives a singple page view of all the ECS services and the health of each service. This can be used to check if all the services are running `steady` on ECS platform or not. If you are willing to check a particular cluster and health of the services inside that cluster, there is a provision to pass cluster name as a `query string parameter` to the API Gateway

Sample URLs are
- **List all the clusters and services:** https://eezs12ee72.execute-api.us-east-1.amazonaws.com/prod/
- **List specific cluster and its services :** https://eezs12ee72.execute-api.us-east-1.amazonaws.com/prod/?cluster=<CLUSTER_NAME>



## Quick Start

1. Update:
    Update `cfn.template` to update following properties
    - Find logical id `LambdaFunction` in the template
    - Update property `Code` with local directory where your clone this repository e.g. C:\aws-automation-plugins\AWSECSInventoryPlugin


2. Run:

       export LAMBDA_BUCKET=<your-lambda-bucket> && ./deploy.sh
    
       or 
    
       SET LAMBDA_BUCKET=<your-lambda-bucket>
       ./deploy.sh



## Stack Details

This stack creates following resources including lambda function and a Rest API Gateway to invoke lambda function. API Gateway URL cna be obtained from the `Output` section on `CloudFormation Console`


### Usage

Lambda function in this project lists all the clusters. Create one thread per cluster and assign following tasks to each thread
-  List all the services of an ECS cluster
- Iterate through the list of services and prepare a batch of 10 services to describe those services in one single API call
- Describe events of each service
- Analyze latest event and mark the service as steady or unsteady based on the matching keyword in an event

> Please note all the AWS API calls are retried using exponential backoff algorithm in case of API throtlling errors.

When you hit API Gateway URL, it generates a `HTML REPORT` which flags unsteady services in RED. This report is useful to get single page view of your ECS inventory and health of ECS services which can help you for monitoring.


### Few of the use cases of this utility are
- If you are stopping your non-prod environment everyday post business hours and starting it before business hours then this utility can help you generate environment health report
- Your developers don't need to sign-in to AWS console just to check if the ECS service they just deployed is stable or not. They can simply hit the `API Gateway URL` for required cluster and can check health of ECS service on their own
- If developers or QA team face any issues during testing they can check health of all the services on their own and figure out issues coming due to unsteady services.
- If you are using EC2-ECS clusters then as part of patching, you have to replace EC2 instances with the new AMI and in this case you can use this utility to check if all the ECS services in that particular cluster are steady post replacing instances with newly patched AMI


## ECS Console Snippet
![image](https://user-images.githubusercontent.com/11420765/138160276-9a5be90c-ac4f-47d5-b801-287525eb2c4b.png)


## Sample Report including all the clusters
![image](https://user-images.githubusercontent.com/11420765/138161391-d166db5f-820e-4851-a042-5d467e1becf8.png)


## Sample report for specific cluster
![image](https://user-images.githubusercontent.com/11420765/138161700-d5e125ab-e66e-47d3-8319-ac94bd045d91.png)


## API Gateway URL
![image](https://user-images.githubusercontent.com/11420765/138163821-435b425b-275a-4d44-a738-f5e36e5bcb72.png)
