from fastapi import APIRouter
from typing import Any
from indicators.rsi import calculate_RSI
from indicators.ma import calculate_moving_average
from indicators.macd import calculate_macd
from indicators.bollinger_bands import get_bollinger_dates
from datetime import datetime
from models.indicator_models import RSI_MADC_ReqBody, MovingAverageReqBody, BollingerBandsReqBody

router: APIRouter = APIRouter(
  prefix = '/ml',
  responses = { 404: { "message": "Endpoint not found!" } }
)

@router.post('/rsi')
async def get_rsi(body: RSI_MADC_ReqBody) -> dict[str, Any]:
  return calculate_RSI(
    body.ticker, 
    datetime.fromisoformat(body.start_date),
    datetime.fromisoformat(body.end_date),
    body.interval
  )

@router.post('/ma')
async def get_ma(body: MovingAverageReqBody) -> dict[str, Any]:
  return calculate_moving_average(
    body.ticker,
    datetime.fromisoformat(body.start_date),
    datetime.fromisoformat(body.end_date),
    body.interval,
    body.day1,
    body.day2
  )

@router.post('/madc')
async def get_madc(body: RSI_MADC_ReqBody) -> dict[str, Any]:
  return calculate_macd(
    body.ticker,
    datetime.fromisoformat(body.start_date),
    datetime.fromisoformat(body.end_date),
    body.interval
  )

@router.post('/bollinger_bands')
async def get_bollinger_bands(body: BollingerBandsReqBody) -> dict[str, Any]:
  return get_bollinger_dates(
    body.crypto,
    body.period,
    body.interval,
    body.window
  )