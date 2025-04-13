from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_ecs_patterns as ecs_patterns,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_iam as iam,
    aws_lambda as lambda_,
    Duration,
    RemovalPolicy,
    Stack,
)
from constructs import Construct
import os
from dotenv import load_dotenv

load_dotenv()

class InformanteLanzamientosStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Obtener variables de entorno
        vpc_id = os.getenv('VPC_ID', 'vpc-0123456789abcdef0')
        table_name = os.getenv('LAUNCHES_TABLE', 'spacex_launches_table')
        repository_name = os.getenv('ECR_REPOSITORY', 'spacex-lanzamientos')

        tabla_lanzamientos = dynamodb.Table(
            self,
            "LaunchesTable",
            table_name=table_name,
            partition_key=dynamodb.Attribute(
                name="launch_id", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        spacex_lambda = lambda_.Function(
            self,
            "SpacexLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="spacex_lambda.manejador_lambda",
            code=lambda_.Code.from_asset("lambda"),
            environment={"LAUNCHES_TABLE": tabla_lanzamientos.table_name},
            timeout=Duration.minutes(5),
        )

        tabla_lanzamientos.grant_read_write_data(spacex_lambda)

        cluster = ecs.Cluster(
            self,
            "SpacexCluster",
            vpc=ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpc_id),
        )

        repository = ecr.Repository(
            self,
            "SpacexRepository",
            repository_name=repository_name,
            removal_policy=RemovalPolicy.DESTROY,
        )

        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "SpacexService",
            cluster=cluster,
            memory_limit_mib=512,
            cpu=256,
            desired_count=2,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_ecr_repository(repository),
                container_port=8000,
                environment={"LAUNCHES_TABLE": tabla_lanzamientos.table_name},
            ),
        )

        tabla_lanzamientos.grant_read_data(fargate_service.task_definition.task_role)
