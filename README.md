# aws-automation-plugins
This repository contains ready to deploy automations on AWS in a region

## How-To

1. All projects in this repository contain a `deploy.sh` file which contains some steps to package the source code and deploy a CloudFormation stack.
Each file expects that you set a `LAMBDA_BUCKET` variable.
Just enter a S3 bucket name where you have access to.
It will be used to upload the code zips for your Lambdas.
2. Finally, just open your command line and execute `$ ./deploy.sh` in the desired folder.
Alternatively, you can use `$ export LAMBDA_BUCKET=<your-bucket-name> && ./deploy.sh`.
3. Test it!
