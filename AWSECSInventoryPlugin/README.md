# AWS CloudWatch Inventory | Cost Optimization

## Pre-Requisites
If you are creating this stack from your local or from EC2 instance, provide necessary permissions on following services to succesfully create stack
- Cloudformation
- S3
- Lambda
- API gateway

---

## Capability
This automation intents to list all the ECS clusters and respective ECS services in a region along with health of each and individual service. Lambda function can be invoked with API Gateway URL `GET` and data will be published in a `HTML Table` on your browser. This report gives a singple page view of all the ECS services and the health of each service. This can be used to check if all the services are running `steady` on ECS platform or not. If you are willing to check a particular cluster and health of the services inside that cluster, there is a provision to pass cluster name as a `query string parameter` to the API Gateway

Sample URLs are
- **List all the clusters and services:** https://eezs12ee72.execute-api.us-east-1.amazonaws.com/prod/
- **List specific cluster and its services :** https://eezs12ee72.execute-api.us-east-1.amazonaws.com/prod/?cluster=<CLUSTER_NAME>

---

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

---

## Stack Details

This stack creates following resources including lambda function and a Rest API Gateway to invoke lambda function. API Gateway URL cna be obtained from the `Output` section on `CloudFormation Console`

---
### Usage

Lambda function in this project lists all the clusters. Create one thread per cluster and assign following tasks to each thread
-  List all the services of an ECS cluster
- Iterate through the list of services and prepare a batch of 10 services to describe those services in one single API call
- Describe events of each service
- Analyze latest event and mark the service as steady or unsteady based on the matching keyword in an event

> Please note all the AWS API calls are retried using exponential backoff algorithm in case of API throtlling errors.

iterates through all the cloudwatch log groups and identify stored bytes of each log group. It then convert stored bytes into human readable format. When you hit API Gateway URL, it generates a `HTML Report` which flags log groups storing GB or TB data in RED. This report is useful to get consolidated view of all log groups and the stored data in Bytes, KB, MB, GB and TB

---

## Sample Report
![image](https://user-images.githubusercontent.com/11420765/135760294-4d9c1f02-17f9-4d23-bf83-84435b6ebcb4.png)

## API Gateway URL
![image](https://user-images.githubusercontent.com/11420765/135760442-7d2837a8-015c-4784-baf7-0f9cd9cbaec8.png)


