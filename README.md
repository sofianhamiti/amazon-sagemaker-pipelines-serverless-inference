# MLOps with Amazon SageMaker for training and AWS Lambda for Serverless Inference

Check out the blog post on Medium: [Deploying a Serverless Inference Service Using Amazon SageMaker Pipelines](https://sofian-hamiti.medium.com/deploying-a-serverless-inference-service-with-amazon-sagemaker-pipelines-2d2f3cc96c39)

## Intro

This is a sample code repository for demonstrating how you can organize your code for deploying an realtime inference Endpoint infrastructure. This code repository is created as part of creating a Project in SageMaker. 

This code repository has the code to find the latest approved ModelPackage for the associated ModelPackageGroup and, once the model approved, it automatically deploys it on a Lambda function exposed by an API Gateway. 

Upon triggering a deployment, the CodePipeline pipeline will deploy 2 API Gateway/Lambda pair - `staging` and `prod`. After the first deployment is completed, the CodePipeline waits for a manual approval step for promotion to the `prod` stage. You will need to go to CodePipeline AWS Managed Console to complete this step.


A description of some of the artifacts is provided below:


### Layout of the SageMaker ModelBuild Project Template

`buildspec.yml`
 - this file is used by the CodePipeline's Build stage to build a CloudFormation template.

`build.py`
 - this python file contains code to get the latest approve package arn and exports staging and configuration files. This is invoked from the Build stage.

`staging-config.json`
 - this configuration file is used to customize `staging` stage in the pipeline. 

`prod-config.json`
 - this configuration file is used to customize `prod` stage in the pipeline. 

`stack`
 - this folder holds the Infrastructure as Code for the staging and production environments. It's written in AWS CDK and Python. The infrastructure uses an Amazon API Gateway and an AWS Lambda: 

![image](https://miro.medium.com/max/2400/1*Pi48flayscFAbZ3vKagREA.png)

`test\buildspec.yml`
  - this file is used by the CodePipeline's `staging` stage to run the test code of the following python file

`test\test.py`
  - this python file contains code to describe and invoke the staging endpoint. You can customize to add more tests here.

## Steps to follow : 

### Step 0 - SageMaker Projects

Go into the console and create the SageMaker Projects for `build, train and deploy` models. Then, go into the details of the Projects and clone locally (on Studio or your IDE) the CodeCommit Repository for `model-deploy`. Once that's done, you can run the Pipeline for Model training. This will take approximately 10 minutes. 

Want to know how to do this step-by-step? Follow Julien Simon's walkthrough on [YouTube](https://www.youtube.com/watch?v=Hvz2GGU3Z8g&feature=emb_title).

### Step 1 - Preparing the repo

Go into the `model-deploy` folder after having cloned locally the repo. Then, you can delete the whole content of the folder, and run this command to replace it with the content of this repo.

```
git clone https://github.com/dgallitelli/amazon-sagemaker-pipelines-serverless-inference
cp amazon-sagemaker-pipelines-serverless-inference/* . -r
rm -rf amazon-sagemaker-pipelines-serverless-inference
```

It should look like this:

![image](https://miro.medium.com/max/2400/1*gYY3IocO1uK2cz3Uur0DlA.png)

Once that's done, you need to create and push the Lambda Container package to ECR:

```
cd container && sh build_and_push.sh <INSERT-NAME-FOR-PACKAGE-HERE>
```

You can now go back into your file system and modify the `stack/stack.py` file, which contains the definition of your CDK stack. In particular, you have to change lines 39 and 44 with the information you get from ECR (the `repository_name` and the `tag`) after having pushed the Docker to ECR.

![image](https://miro.medium.com/max/521/1*q-2QApN_gatw0mpC7qp1cQ.png)

Now, you have to push the modification to CodeCommit. In Studio, you can do this from the Git tab. Make sure to actually push, not just commit.

Make sure your `AmazonSageMakerServiceCatalogProductsUseRole` in AWS IAM looks like this:

![image](https://miro.medium.com/max/571/1*NpCKyFrQ1Q4mTDPjtBcNYg.png)

### Step 2 - Approve the model from Model Registry

![image](https://miro.medium.com/max/700/1*HrIa7Thc0KLnBHFQVHvy_Q.png)

### Step 3 - See the stack getting deployed from CodePipeline

### (Optional) Step 4 - Test the endpoint

Use this payload to test the endpoint in Postman or anything you prefer.

```json
{
    "length": -0.158164,
    "diameter": -0.280982,
    "height": -0.227545,
    "whole_weight": -0.352298,
    "shucked_weight": -0.596421,
    "viscera_weight": -0.019102,
    "shell_weight": -0.135293,
    "sex_M": 0.0,
    "sex_F": 0.0,
    "sex_I": 1.0
}
```