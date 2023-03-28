import { IsNotEmpty } from "class-validator"

export class RSI_MADC_RequestModel {
  @IsNotEmpty() ticker: string
  @IsNotEmpty() interval: string
  @IsNotEmpty() start_date: string
  @IsNotEmpty() end_date: string
}

export class MovingAverageRequestModel extends RSI_MADC_RequestModel {
  @IsNotEmpty() day1: number
  @IsNotEmpty() day2: number
}

export class BollingerBandsRequestBody {
  @IsNotEmpty() crypto: string
  @IsNotEmpty() period: string
  @IsNotEmpty() interval: string
  @IsNotEmpty() window: number
}