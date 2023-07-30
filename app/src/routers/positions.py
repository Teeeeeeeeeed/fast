import json
from fastapi import APIRouter, BackgroundTasks, Depends, WebSocket, WebSocketDisconnect
from app.src.schema.satellite import TrajectoryRequest
from app.src.services.position_stream_manager import PositionStream, PositionStreamManager
from app.src.services.satellite_service import SatelliteService

position_router = APIRouter(tags=["Positions"], prefix="/positions")

@position_router.websocket("/get-position-stream/{client_id}")
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

@position_router.post("/get-trajectories")
async def get_trajectory(body: TrajectoryRequest, satelliteService: SatelliteService = Depends()):
    return satelliteService.get_trajectories(body.ids)