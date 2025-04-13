import json
import os
import boto3
import requests
from datetime import datetime
from typing import Dict, List, Any

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['LAUNCHES_TABLE'])

def obtener_lanzamientos_spacex() -> List[Dict[str, Any]]:
    url = "https://api.spacexdata.com/v4/launches"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def procesar_datos_lanzamiento(lanzamiento: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'launch_id': lanzamiento['id'],
        'mission_name': lanzamiento['name'],
        'rocket_name': lanzamiento['rocket']['name'],
        'launch_date': lanzamiento['date_utc'],
        'status': 'success' if lanzamiento['success'] else 'failed',
        'launch_site': lanzamiento['launchpad']['name'],
        'details': lanzamiento.get('details', ''),
        'payloads': [p['id'] for p in lanzamiento.get('payloads', [])],
        'updated_at': datetime.utcnow().isoformat()
    }

def manejador_lambda(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        lanzamientos = obtener_lanzamientos_spacex()
        
        lanzamientos_procesados = []
        for lanzamiento in lanzamientos:
            lanzamiento_procesado = procesar_datos_lanzamiento(lanzamiento)
            
            table.put_item(Item=lanzamiento_procesado)
            lanzamientos_procesados.append(lanzamiento_procesado)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Procesados {len(lanzamientos_procesados)} lanzamientos exitosamente',
                'launches': lanzamientos_procesados
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        } 