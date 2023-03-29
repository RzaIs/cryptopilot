import { IsNotEmpty } from "class-validator"

export class RSI_MADC_RequestModel {
  @IsNotEmpty() ticker: string
  @IsNotEmpty() interval: string

  start_date: string
  end_date: string
}

export class MovingAverageRequestModel {
  @IsNotEmpty() day1: number
  @IsNotEmpty() day2: number
  @IsNotEmpty() ticker: string
  @IsNotEmpty() interval: string

  start_date: string
  end_date: string
}

export class BollingerBandsRequestBody {
  @IsNotEmpty() crypto: string
  @IsNotEmpty() interval: string
  @IsNotEmpty() window: number

  start_date: string
  end_date: string
}

export class StochasticRequestBody {
  @IsNotEmpty() ticker: string
  @IsNotEmpty() start_date: string

  end_date: string
  interval: string
}

export class EmaCrossRequestBody {
  @IsNotEmpty() ticker: string
  @IsNotEmpty() interval: string
  @IsNotEmpty() slow: number
  @IsNotEmpty() fast: number

  start_date: string
  end_date: string
}

export class CryptoValueRequestBody {
  @IsNotEmpty() ticker: string
  @IsNotEmpty() interval: string

  start_date: string
  end_date: string
}
  
