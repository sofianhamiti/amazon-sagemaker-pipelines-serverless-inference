# MLOps with Amazon SageMaker for training and AWS Lambda for Serverless Inference

Check out the blog post on Medium: [Deploying a Serverless Inference Service Using Amazon SageMaker Pipelines](https://sofian-hamiti.medium.com/deploying-a-serverless-inference-service-with-amazon-sagemaker-pipelines-2d2f3cc96c39)

## Intro

This is a sample code repository for demonstrating how you can organize your code for deploying an realtime inference Endpoint infrastructure. This code repository is created as part of creating a Project in SageMaker. 

This code repository has the code to find the latest approved ModelPackage for the associated ModelPackageGroup and automaticaly deploy it to the Endpoint on detecting a change (`build.py`). This code repository also defines the CloudFormation template which defines the Endpoints as infrastructure. It also has configuration files associated with `staging` and `prod` stages. 

Upon triggering a deployment, the CodePipeline pipeline will deploy 2 Endpoints - `staging` and `prod`. After the first deployment is completed, the CodePipeline waits for a manual approval step for promotion to the prod stage. You will need to go to CodePipeline AWS Managed Console to complete this step.

You own this code and you can modify this template to change as you need it, add additional tests for your custom validation. 

A description of some of the artifacts is provided below:


### Layout of the SageMaker ModelBuild Project Template

`buildspec.yml`
 - this file is used by the CodePipeline's Build stage to build a CloudFormation template.

`build.py`
 - this python file contains code to get the latest approve package arn and exports staging and configuration files. This is invoked from the Build stage.

`endpoint-config-template.yml`
 - this CloudFormation template file is packaged by the build step in the CodePipeline and is deployed in different stages.

`staging-config.json`
 - this configuration file is used to customize `staging` stage in the pipeline. You can configure the instance type, instance count here.

`prod-config.json`
 - this configuration file is used to customize `prod` stage in the pipeline. You can configure the instance type, instance count here.

`test\buildspec.yml`
  - this file is used by the CodePipeline's `staging` stage to run the test code of the following python file

`test\test.py`
  - this python file contains code to describe and invoke the staging endpoint. You can customize to add more tests here.

## Steps to follow : 

### Step 0 - SageMaker Projects

Go into the console and create the SageMaker Projects for `build, train and deploy` models. Then, go into the details of the Projects and clone locally (on Studio or your IDE) the CodeCommit Repository for `model-deploy`. Once that's done, you can run the Pipeline for Model training. This will take approximately 10 minutes. 

### Step 1 - Preparing the repo

Go into the `model-deploy` folder after having cloned locally the repo. Then, run in a CLI these commands:

```
git clone https://github.com/dgallitelli/amazon-sagemaker-pipelines-serverless-inference
cp amazon-sagemaker-pipelines-serverless-inference/* . -r
rm -rf amazon-sagemaker-pipelines-serverless-inference
```

Once that's done, you need to create and push the Lambda Container package to ECR:

```
cd container && sh build_and_push.sh <INSERT-NAME-FOR-PACKAGE-HERE>
```

You can now go back into your file system and modify the `stack/stack.py` file, which contains the definition of your CDK stack. In particular, you have to change lines 39 and 44 with the information you get from ECR (the `repository_name` and the `tag`) after having pushed the Docker to ECR.

Now, you have to push the modification to CodeCommit. In Studio, you can do this from the Git tab. Make sure to actually push, not just commit.

### Step 2 - Approve the model from Model Registry

### Step 3 - See the stack getting deployed from CodePipeline

### (Optional) Step 4 - Test the endpoint