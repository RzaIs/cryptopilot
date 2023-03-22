from pydantic import BaseModel

class RSI_ReqBody(BaseModel):
  ticker: str
  interval: str

class MovingAverageReqBody(RSI_ReqBody):
  day1: int
  day2: int