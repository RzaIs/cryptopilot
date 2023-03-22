import { IsNotEmpty } from "class-validator"

export class RSIRequestModel {
  @IsNotEmpty() ticker: string
  @IsNotEmpty() interval: string
}

export class MovingAverageRequestModel extends RSIRequestModel {
  @IsNotEmpty() day1: number
  @IsNotEmpty() day2: number
}