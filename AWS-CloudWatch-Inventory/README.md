# AWS CloudWatch Inventory | Cost Optimization

## Pre-Requisites
If you are creating this stack from your local or from EC2 instance, provide necessary permissions on following services to succesfully create stack
- Cloudformation
- S3
- Lambda
- API gateway

## Capability
This automation intents to list all the cloudwatch log groups in a region and data-size of each log group. Lambda function can be invoked with API Gateway URL `GET` and data will be published in a `HTML Table` on your browser. This data is useful to identify log groups with high data ingestion and stored bytes. This can be used to take necessary actions for cost optimization in CloudWatch. Sample report and a CloudFormation console snapshot is attached in the last section on this page.

## Quick Start

1. Update:
    Update `cfn.template` to update following properties
    - Find logical id `LambdaFunction` in the template
    - Update property `Code` with local directory where your clone this repository e.g. C:\aws-automation-plugins\AWS-CloudWatch-Inventory 


2. Run:

       export LAMBDA_BUCKET=<your-lambda-bucket> && ./deploy.sh
    
       or 
    
       SET LAMBDA_BUCKET=<your-lambda-bucket>
       ./deploy.sh

## Stack Details

This stack creates following resources including lambda function and a Rest API Gateway to invoke lambda function. API Gateway URL cna be obtained from the `Output` section on `CloudFormation Console`


### Usage

Lambda function in this project iterates through all the cloudwatch log groups and identify stored bytes of each log group. It then convert stored bytes into human readable format. When you hit API Gateway URL, it generates a `HTML Report` which flags log groups storing GB or TB data in RED. This report is useful to get consolidated view of all log groups and the stored data in Bytes, KB, MB, GB and TB

## Sample Report
![image](https://user-images.githubusercontent.com/11420765/135760294-4d9c1f02-17f9-4d23-bf83-84435b6ebcb4.png)

## API Gateway URL
![image](https://user-images.githubusercontent.com/11420765/135760442-7d2837a8-015c-4784-baf7-0f9cd9cbaec8.png)


