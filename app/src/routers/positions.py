import json
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from src.database.db import get_db_connection
from src.schema.satellite import TrajectoryRequest
from src.services.position_stream_manager import PositionStream, PositionStreamManager
from src.services.satellite_service import SatelliteService

position_router = APIRouter(tags=["Positions"])

@position_router.websocket("/api/ws/positions/get-position-stream/{client_id}")
async def get_position(client_id:str, websocket: WebSocket, connectionManager: PositionStreamManager = Depends()):
    await websocket.accept()
    connectionManager.set_client(client_id, PositionStream(websocket, []))
    try:
        while True:
            data = await websocket.receive_text()
            satellites_to_track = [int(num) for num in json.loads(data)]
            connectionManager.get_client(client_id).satellites_to_track = satellites_to_track
            await connectionManager.update_clients(client_id)

    except WebSocketDisconnect:
        connectionManager.del_client(client_id)
        websocket.close()

@position_router.post("/api/positions/get-trajectories")
async def get_trajectory(body: TrajectoryRequest, session = Depends(get_db_connection), satelliteService: SatelliteService = Depends()):
    return satelliteService.get_trajectories(body.ids, session)

@position_router.post("/api/positions/get-position-stream")
async def get_position(body: TrajectoryRequest, session = Depends(get_db_connection), satelliteService: SatelliteService = Depends()):
    return satelliteService.get_positions(body.ids, session)