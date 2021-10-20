#!/usr/bin/env bash

LAMBDA_BUCKET="${LAMBDA_BUCKET}"
STACK_NAME="ECSInventoryStack"

if [[ "${LAMBDA_BUCKET}" == "" || "${STACK_NAME}" == "" ]]; then
    echo "You must set LAMBDA_BUCKET and STACK_NAME first."
    exit 1;
fi

aws cloudformation package --template-file cfn.template --s3-bucket ${LAMBDA_BUCKET} --output-template-file cfn.packaged.template
aws cloudformation deploy --template-file cfn.packaged.template --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM