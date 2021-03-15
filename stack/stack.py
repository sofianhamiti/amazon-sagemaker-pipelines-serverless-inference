from aws_cdk import (
    aws_iam as iam,
    aws_ecr as ecr,
    aws_lambda,
    aws_apigatewayv2 as apigw,
    core
)


class InferenceStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ==================================================
        # =============== CFN PARAMETERS ===================
        # ==================================================
        project_name = core.CfnParameter(scope=self, id='SageMakerProjectName', type='String')
        model_execution_role_arn = core.CfnParameter(scope=self, id='ModelExecutionRoleArn', type='String')
        model_binary_location = core.CfnParameter(scope=self, id='ModelBinaryLocation', type='String')
        stage_name = core.CfnParameter(scope=self, id='StageName', type='String')

        name = f'{project_name.value_as_string}-{stage_name.value_as_string}'
        # ==================================================
        # ================== IAM ROLE ======================
        # ==================================================
        role = iam.Role.from_role_arn(
            scope=self,
            id='role',
            role_arn=model_execution_role_arn.value_as_string
        )

        # ==================================================
        # ================== ECR IMAGE =====================
        # ==================================================
        ecr_repository = ecr.Repository.from_repository_name(
            scope=self,
            id='repo',
            repository_name='<ADD YOUR CONTAINER REPO HERE>'
        )

        ecr_image = aws_lambda.DockerImageCode.from_ecr(
            repository=ecr_repository,
            tag='<ADD YOUR IMAGE TAG HERE>'
        )
        # ==================================================
        # ================ LAMBDA FUNCTION =================
        # ==================================================
        lambda_function = aws_lambda.DockerImageFunction(
            scope=self,
            id='lambda',
            function_name=name,
            code=ecr_image,
            memory_size=1024,
            role=role,
            environment={
                'MODEL_S3_URI': model_binary_location.value_as_string,
            },
            timeout=core.Duration.seconds(60)
        )

        # ==================================================
        # ================== API GATEWAY ===================
        # ==================================================
        api = apigw.HttpApi(
            scope=self,
            id='api_gateway',
            api_name=name,
            cors_preflight={
                "allow_headers": ["Authorization"],
                "allow_methods": [apigw.HttpMethod.POST],
                "allow_origins": ["*"],
                "max_age": core.Duration.days(10)
            }
        )

        integration = apigw.CfnIntegration(
            scope=self,
            id='integration',
            api_id=api.http_api_id,
            credentials_arn=role.role_arn,
            integration_type='AWS_PROXY',
            integration_uri=lambda_function.function_arn,
            integration_method='POST',
            payload_format_version='2.0'
        )

        apigw.CfnRoute(
            scope=self,
            id='route',
            api_id=api.http_api_id,
            route_key='POST /',
            target=f'integrations/{integration.ref}'
        )


app = core.App()
InferenceStack(app, "inference")

app.synth()
