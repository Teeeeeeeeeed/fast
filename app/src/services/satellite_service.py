from fastapi import Depends

from ..clients.noradclient import NoradClient, get_norad_client

async def search_satellite(
        norad_id:int, 
        norad_client:NoradClient = Depends(get_norad_client)):
    response = await norad_client.searchTLE(norad_id)
    return response