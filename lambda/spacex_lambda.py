import json
import os
import boto3
import requests
from datetime import datetime
from typing import Dict, List, Any

dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table(os.environ['TABLA_LANZAMIENTOS'])

def obtener_lanzamientos_spacex() -> List[Dict[str, Any]]:
    url = "https://api.spacexdata.com/v4/launches"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def procesar_datos_lanzamiento(lanzamiento: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'id_lanzamiento': lanzamiento['id'],
        'nombre_mision': lanzamiento['name'],
        'fecha_lanzamiento': lanzamiento['date_utc'],
        'nombre_cohete': lanzamiento['rocket']['name'],
        'sitio_lanzamiento': lanzamiento['launchpad']['name'],
        'lanzamiento_exitoso': lanzamiento.get('success', False),
        'proximo': lanzamiento['upcoming'],
        'detalles': lanzamiento.get('details', ''),
        'enlaces': {
            'webcast': lanzamiento.get('links', {}).get('webcast', ''),
            'articulo': lanzamiento.get('links', {}).get('article', ''),
            'wikipedia': lanzamiento.get('links', {}).get('wikipedia', '')
        },
        'updated_at': datetime.utcnow().isoformat()
    }

def lambda_handler(event, context):
    """Manejador principal de la función Lambda"""
    try:
        # Obtener datos de la API de SpaceX
        respuesta = requests.get('https://api.spacexdata.com/v4/launches')
        lanzamientos = respuesta.json()
        
        # Procesar cada lanzamiento
        for lanzamiento in lanzamientos:
            item = procesar_datos_lanzamiento(lanzamiento)
            
            # Guardar en DynamoDB
            tabla.put_item(Item=item)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': f'Se procesaron {len(lanzamientos)} lanzamientos exitosamente'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error al procesar los lanzamientos: {str(e)}'
            })
        } 