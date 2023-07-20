from pydantic import BaseModel


class NoradInfo(BaseModel):
    satid: int
    satname: str
    transactionscount: int 

class NoradResponse(BaseModel):
    info: NoradInfo
    tle: str