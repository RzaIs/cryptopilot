import { Injectable } from "@nestjs/common";
import { Axios, msaxios } from "src/helper/ms.axios";
import { MovingAverageRequestModel, RSIRequestModel } from "./data.models";

@Injectable()
export class DataService {
  async getRSIs(body: RSIRequestModel): Promise<unknown> {
    return (await msaxios(() => {
      return Axios.post('/ml/rsi', body)
    })).data
  }

  async getMovingAverage(body: MovingAverageRequestModel): Promise<unknown>  {
    return (await msaxios(() => {
      return Axios.post('/ml/ma', body)
    })).data
  }
}