from httpx import Client, HTTPError, Response
from dotenv import dotenv_values

class NoradClient:
    def __init__(self) -> None:
        self.session = Client()
        self.session.headers.update({"Content-Type": "application/json"})
        env_variables = dotenv_values(".env")
        self.api_key = env_variables["NORAD_API_KEY"]
        self.base_url = env_variables["NORAD_API_URL"]

    async def _perform_request(self, method: str, path: str, *args, **kwargs) -> Response:
        res = None
        try:
            res = getattr(self.session, method)(
                f"{self.base_url}{path}", *args, **kwargs
            )  # 2
            res.raise_for_status()  # 3
        except HTTPError:
            raise self.base_error(
                f"{self.__class__.__name__} request failure:\n"
                f"{method.upper()}: {path}\n"
                f"Message: {res is not None and res.text}",
                raw_response=res,
            )
        return res

    async def searchTLE(self, norad_id:int):
        url = f"/tle/{norad_id}&apiKey={self.api_key}"
        response = await self._perform_request("get", url)
        return response.json()
     
    def __del__(self):
        self.session.close()

norad_client = NoradClient()

async def get_norad_client() -> NoradClient:
    return norad_client