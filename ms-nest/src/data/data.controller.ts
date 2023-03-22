import { Body, Controller, Post, UseGuards } from "@nestjs/common";
import { AuthStrategy } from "src/auth/auth.strategy";
import { executeAsync } from "src/helper/service.executer";
import { MovingAverageRequestModel, RSIRequestModel } from "./data.models";
import { DataService } from "./data.service";

@UseGuards(AuthStrategy.JwtGuard)
@Controller('data')
export class DataController {
  constructor(private readonly service: DataService) { }

  @Post('rsi')
  async getRSIs(@Body() body: RSIRequestModel): Promise<unknown> {
    return executeAsync(this.service.getRSIs(body))
  }

  @Post('ma')
  async getMovingAverage(@Body() body: MovingAverageRequestModel): Promise<unknown> {
    return executeAsync(this.service.getMovingAverage(body))
  }
}