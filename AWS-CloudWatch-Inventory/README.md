# AWS CloudWatch Inventory | Cost Optimization | Automation

## Pre-Requisites
If you are creating this stack from your local or from EC2 instance, provide necessary permissions on following services to succesfully create stack
- Cloudformation
- S3
- Lambda
- API gateway

## Capability
This automation intents to list all the cloudwatch log groups in a region and data-size of each log group. Lambda function can be invoked with API Gateway URL `GET` and data will be published in a `HTML Table` on your browser. This data is useful to identify log groups with high data ingestion and stored bytes. This can be used to take necessary actions for cost optimization in CloudWatch

## Quick Start

Run:

    export LAMBDA_BUCKET=<your-lambda-bucket> && ./deploy.sh
    
    or 
    
    SET LAMBDA_BUCKET=<your-lambda-bucket>
    ./deploy.sh


## Stack Details

This stack creates following resources including lambda function and a Rest API Gateway to invoke lambda function. API Gateway URL cna be obtained from the `Output` section on `CloudFormation Console`


### Usage

Lambda function in this project iterates through all the cloudwatch log groups and identify stored bytes of each log group. It then convert stored bytes into human readable format. When you hit API Gateway URL, it generates a `HTML Report` which flags log groups storing GB or TB data in RED. This report is useful to get consolidated view of all log groups and the stored data in Bytes, KB, MB, GB and TB

