from pydantic import BaseModel

class RSI_MADC_ReqBody(BaseModel):
  ticker: str
  interval: str
  start_date: str | None
  end_date: str | None

class MovingAverageReqBody(BaseModel):
  ticker: str
  interval: str
  day1: int
  day2: int
  start_date: str | None
  end_date: str | None

class BollingerBandsReqBody(BaseModel):
  crypto: str
  interval: str
  window: int
  start_date: str | None
  end_date: str | None

class StochasticReqBody(BaseModel):
  ticker: str
  interval: str
  start_date: str | None
  end_date: str | None

class EMACrossReqBody(BaseModel):
  ticker: str
  interval: str
  slow: int
  fast: int
  start_date: str | None
  end_date: str | None

class CryptoValueReqBody(BaseModel):
  ticker: str
  interval: str
  start_date: str | None
  end_date: str | None
