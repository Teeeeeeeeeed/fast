from typing import List
from fastapi import Depends, FastAPI, WebSocket
from src.database.models import Satellite

from src.services.satellite_service import SatelliteService

app = FastAPI()

class PositionStream:
    websocket: WebSocket
    satellites_to_track: List[str]

    def __init__(self, websocket:WebSocket, satellites_to_track: List[str]) -> None:
        self.websocket = websocket
        self.satellites_to_track = satellites_to_track

class PositionStreamManager:
    satellite_service: SatelliteService
    __connected_clients = {}
    backgroundTask = None

    def __init__(self, satelliteService: SatelliteService = Depends()) -> None:
        self.satellite_service = satelliteService

    def set_client(self, client_id: str, stream: PositionStream):
        self.__connected_clients[client_id] = stream

    def get_client(self, client_id: str) -> PositionStream:
        return self.__connected_clients[client_id]
    
    def del_client(self, client_id: str):
        del self.__connected_clients[client_id]

    async def update_clients(self, client_id: str):
        stream:PositionStream = self.__connected_clients.get(client_id)
        satellites:List[Satellite] = stream.satellites_to_track
        positions = self.satellite_service.get_positions(satellites)
        ws: WebSocket = stream.websocket
        await ws.send_json(positions)

stream_manager = PositionStreamManager()

