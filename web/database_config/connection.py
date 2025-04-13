import os
import boto3
from typing import Generator, Any

# Configuración BD
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['LAUNCHES_TABLE'])

def get_db() -> Generator[Any, None, None]:
    try:
        yield table
    finally:
        pass

class Base:
    metadata = None