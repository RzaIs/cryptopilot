import { Body, Controller, Post, UseGuards } from "@nestjs/common";
import { AuthStrategy } from "src/auth/auth.strategy";
import { executeAsync } from "src/helper/service.executer";
import { BollingerBandsRequestBody, CryptoValueRequestBody, EmaCrossRequestBody, MovingAverageRequestModel, RSI_MADC_RequestModel, StochasticRequestBody } from "./data.models";
import { DataService } from "./data.service";

@UseGuards(AuthStrategy.JwtGuard)
@Controller('data')
export class DataController {
  constructor(private readonly service: DataService) { }

  @Post('rsi')
  async getRSI(@Body() body: RSI_MADC_RequestModel): Promise<unknown> {
    return executeAsync(this.service.getRSI(body))
  }

  @Post('ma')
  async getMovingAverage(@Body() body: MovingAverageRequestModel): Promise<unknown> {
    return executeAsync(this.service.getMovingAverage(body))
  }

  @Post('madc')
  async getMADC(@Body() body: RSI_MADC_RequestModel): Promise<unknown> {
    return executeAsync(this.service.getMADC(body))
  }

  @Post('bollinger_bands')
  async getBollingerBands(@Body() body: BollingerBandsRequestBody): Promise<unknown> {
    return executeAsync(this.service.getBollingerBands(body))
  }

  @Post('stochastic')
  async getStochasticOscillator(@Body() body: StochasticRequestBody): Promise<unknown> {
    return executeAsync(this.service.getStochasticOscillator(body))
  }

  @Post('ema')
  async getEmaCross(@Body() body: EmaCrossRequestBody): Promise<unknown> {
    return executeAsync(this.service.getEmaCross(body))
  }

  @Post('cryptos')
  async getCryptoValues(@Body() body: CryptoValueRequestBody): Promise<unknown> {
    return executeAsync(this.service.getCryptoValues(body))
  }
}