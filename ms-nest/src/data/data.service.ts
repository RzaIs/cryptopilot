import { Injectable } from "@nestjs/common";
import { Axios, msaxios } from "src/helper/ms.axios";
import { BollingerBandsRequestBody, MovingAverageRequestModel, RSI_MADC_RequestModel } from "./data.models";

@Injectable()
export class DataService {
  async getRSI(body: RSI_MADC_RequestModel): Promise<unknown> {
    return (await msaxios(() => {
      return Axios.post('/ml/rsi', body)
    })).data
  }

  async getMovingAverage(body: MovingAverageRequestModel): Promise<unknown>  {
    return (await msaxios(() => {
      return Axios.post('/ml/ma', body)
    })).data
  }

  async getMADC(body: RSI_MADC_RequestModel): Promise<unknown> {
    return (await msaxios(() => {
      return Axios.post('/ml/madc', body)
    })).data
  }

  async getBollingerBands(body: BollingerBandsRequestBody): Promise<unknown> {
    return (await msaxios(() => {
      return Axios.post('/ml/bollinger_bands', body)
    })).data
  }
}