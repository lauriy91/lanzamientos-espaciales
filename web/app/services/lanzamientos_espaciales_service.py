from typing import List, Dict, Any
from datetime import datetime
import boto3
import os
from fastapi import HTTPException


class LanzamientosEspacialesService:
    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(os.environ["LAUNCHES_TABLE"])

    async def get_all_launches(self, db: Any) -> List[Dict[str, Any]]:
        try:
            response = self.table.scan()
            return response.get("Items", [])
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_launch_by_id(self, db: Any, launch_id: str) -> Dict[str, Any]:
        try:
            response = self.table.get_item(Key={"launch_id": launch_id})
            if "Item" not in response:
                raise HTTPException(status_code=404, detail="Lanzamiento no encontrado")
            return response["Item"]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_rocket_statistics(self, db: Any) -> Dict[str, Any]:
        try:
            response = self.table.scan()
            launches = response.get("Items", [])

            stats = {}
            for launch in launches:
                rocket = launch["rocket_name"]
                if rocket not in stats:
                    stats[rocket] = {"total": 0, "exitosos": 0, "fallidos": 0}
                stats[rocket]["total"] += 1
                if launch["status"] == "success":
                    stats[rocket]["exitosos"] += 1
                else:
                    stats[rocket]["fallidos"] += 1

            return stats
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_launch_status_statistics(self, db: Any) -> Dict[str, Any]:
        try:
            response = self.table.scan()
            launches = response.get("Items", [])

            stats = {
                "total": len(launches),
                "exitosos": 0,
                "fallidos": 0,
                "proximos": 0,
            }

            for launch in launches:
                if launch["status"] == "success":
                    stats["exitosos"] += 1
                elif launch["status"] == "failed":
                    stats["fallidos"] += 1
                else:
                    stats["proximos"] += 1

            return stats
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_upcoming_launches(self, db: Any) -> List[Dict[str, Any]]:
        try:
            response = self.table.scan()
            launches = response.get("Items", [])

            # Filtrar proximos lanzamientos junto a sus fechas
            now = datetime.utcnow()
            upcoming = [
                launch
                for launch in launches
                if datetime.fromisoformat(launch["launch_date"]) > now
            ]
            upcoming.sort(key=lambda x: x["launch_date"])

            return upcoming
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
