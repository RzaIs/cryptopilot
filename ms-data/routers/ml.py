from fastapi import APIRouter
from typing import Any
from indicators.rsi import calculate_RSI
from indicators.ma import calculate_moving_average
from models.indicator_models import RSI_ReqBody, MovingAverageReqBody

router: APIRouter = APIRouter(
  prefix = '/ml',
  responses = { 404: { "message": "Endpoint not found!" } }
)

@router.post('/rsi')
async def get_rsi(body: RSI_ReqBody) -> dict[str, Any]:
  return calculate_RSI(
    body.ticker, 
    body.interval
  )

@router.post('/ma')
async def get_ma(body: MovingAverageReqBody) -> dict[str, Any]:
  return calculate_moving_average(
    body.ticker,
    body.interval,
    body.day1,
    body.day2
  )