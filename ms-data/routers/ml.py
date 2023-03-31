from fastapi import APIRouter
from typing import Any
from indicators.rsi import calculate_RSI
from indicators.moving_average import calculate_moving_average
from indicators.madc import calculate_macd
from indicators.bollinger_bands import get_bollinger_dates
from indicators.stochastic_oscillator import calculate_stochastic_oscillator
from indicators.backtest_ema import EMA_cross
from indicators.crypto_values import value as crypto_value
from datetime import datetime
from models.indicator_models import (
  RSI_MADC_ReqBody,
  MovingAverageReqBody,
  BollingerBandsReqBody,
  StochasticReqBody,
  EMACrossReqBody,
  CryptoValueReqBody
)

router: APIRouter = APIRouter(
  prefix = '/ml',
  responses = { 404: { "message": "Endpoint not found!" } }
)

@router.post('/rsi')
async def get_rsi(body: RSI_MADC_ReqBody) -> dict[str, Any]:
  return calculate_RSI(
    body.ticker, 
    body.interval,
    body.start_date,
    body.end_date,
  )

@router.post('/ma')
async def get_ma(body: MovingAverageReqBody) -> dict[str, Any]:
  return calculate_moving_average(
    body.ticker,
    datetime.fromisoformat(body.start_date),
    datetime.fromisoformat(body.end_date),
    body.interval,
    body.day1,
    body.day2,
  )

@router.post('/madc')
async def get_madc(body: RSI_MADC_ReqBody) -> dict[str, Any]:
  return calculate_macd(
    body.ticker,
    body.interval,
    body.start_date,
    body.end_date
  )

@router.post('/bollinger_bands')
async def get_bollinger_bands(body: BollingerBandsReqBody) -> dict[str, Any]:
  return get_bollinger_dates(
    body.crypto,
    body.interval,
    body.start_date,
    body.end_date,
    body.window,
  )

@router.post('/stochastic')
async def get_stochastic_oscillator(body: StochasticReqBody) -> dict[str, Any]:
  return calculate_stochastic_oscillator(
    body.ticker,
    body.interval,
    body.start_date,
    body.end_date,
  )

@router.post('/ema')
async def get_ema_cross(body: EMACrossReqBody) -> dict[str, Any]:
  return EMA_cross(
    body.ticker,
    body.interval,
    body.start_date,
    body.end_date,
    body.slow,
    body.fast,
  )

@router.post('/cryptos')
async def get_crypto_values(body: CryptoValueReqBody) -> dict[str, Any]:
  return crypto_value(
    body.ticker,
    body.interval,
    body.start_date,
    body.end_date,
  )