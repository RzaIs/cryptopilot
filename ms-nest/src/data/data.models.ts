import { IsNotEmpty, IsOptional } from "class-validator"

export class RSI_MADC_RequestModel {
  @IsNotEmpty() ticker: string
  @IsNotEmpty() interval: string

  @IsOptional() start_date: string
  @IsOptional() end_date: string
}

export class MovingAverageRequestModel {
  @IsNotEmpty() day1: number
  @IsNotEmpty() day2: number
  @IsNotEmpty() ticker: string
  @IsNotEmpty() interval: string

  @IsOptional() start_date: string
  @IsOptional() end_date: string
}

export class BollingerBandsRequestBody {
  @IsNotEmpty() crypto: string
  @IsNotEmpty() interval: string
  @IsNotEmpty() window: number

  @IsOptional() start_date: string
  @IsOptional() end_date: string
}

export class StochasticRequestBody {
  @IsNotEmpty() ticker: string
  @IsNotEmpty() start_date: string

  @IsOptional() end_date: string
  @IsOptional() interval: string
}

export class EmaCrossRequestBody {
  @IsNotEmpty() ticker: string
  @IsNotEmpty() interval: string
  @IsNotEmpty() slow: number
  @IsNotEmpty() fast: number

  @IsOptional() start_date: string
  @IsOptional() end_date: string
}

export class CryptoValueRequestBody {
  @IsNotEmpty() ticker: string
  @IsNotEmpty() interval: string

  @IsOptional() start_date: string
  @IsOptional() end_date: string
}
  