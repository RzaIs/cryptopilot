import axios, { AxiosError } from "axios"
import { some } from "./optional"

export const Axios = axios.create({
  baseURL: process.env.MS_DATA_URL,
  headers: {
    BRIDGE_SECRET: process.env.BRIDGE_SECRET
  }
})

export async function msaxios<T>(networkCall: () => Promise<{ data: T }>): Promise<{ data: T }> {
  try {
    return await networkCall()
  } catch (error) {
    if (error instanceof AxiosError && some(error.response)) {
      return error.response
    } else {
      throw error
    }
  }
}