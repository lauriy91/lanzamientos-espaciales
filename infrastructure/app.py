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

class PilaInformanteLanzamientos(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Obtener variables de entorno
        vpc_id = os.getenv('VPC_ID', 'vpc-0123456789abcdef0')
        nombre_tabla = os.getenv('TABLA_LANZAMIENTOS', 'tabla_lanzamientos_spacex')
        nombre_repositorio = os.getenv('REPOSITORIO_ECR', 'lanzamientos-spacex')

        tabla_lanzamientos = dynamodb.Table(
            self,
            "TablaLanzamientos",
            nombre_tabla=nombre_tabla,
            partition_key=dynamodb.Attribute(
                name="id_lanzamiento", type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
            point_in_time_recovery=False,
            server_side_encryption=False,
        )

        lambda_spacex = lambda_.Function(
            self,
            "LambdaSpacex",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="manejador_lambda.lambda_handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={"TABLA_LANZAMIENTOS": tabla_lanzamientos.nombre_tabla},
            timeout=Duration.minutes(1),
            memory_size=128,
        )

        tabla_lanzamientos.grant_read_write_data(lambda_spacex)

        cluster = ecs.Cluster(
            self,
            "ClusterSpacex",
            vpc=ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpc_id),
            container_insights=False,
        )

        repositorio = ecr.Repository(
            self,
            "RepositorioSpacex",
            nombre_repositorio=nombre_repositorio,
            removal_policy=RemovalPolicy.DESTROY,
            lifecycle_rules=[],
            image_scan_on_push=False,
        )

        servicio_fargate = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "ServicioSpacex",
            cluster=cluster,
            memory_limit_mib=256,
            cpu=128,
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_ecr_repository(repositorio),
                container_port=8000,
                environment={"TABLA_LANZAMIENTOS": tabla_lanzamientos.nombre_tabla},
            ),
        )

        tabla_lanzamientos.grant_read_data(servicio_fargate.task_definition.task_role)
