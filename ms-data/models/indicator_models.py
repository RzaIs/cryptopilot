from pydantic import BaseModel

class RSI_MADC_ReqBody(BaseModel):
  ticker: str
  interval: str
  start_date: str
  end_date: str

class MovingAverageReqBody(RSI_MADC_ReqBody):
  day1: int
  day2: int

class BollingerBandsReqBody(BaseModel):
  crypto: str
  period: str
  interval: str
  window: int

class StochasticReqBody(BaseModel):
  ticker: str
  start_date: str
  end_date: str
  interval: str

class EMACrossReqBody(BaseModel):
  ticker: str
  start_date: str
  end_date: str
  interval: str
  slow: int
  fast: int

class CryptoValueReqBody(BaseModel):
  ticker: str
  start_date: str
  end_date: str
  interval: str
