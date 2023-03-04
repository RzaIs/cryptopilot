import { AxiosError } from "axios"
import { some } from "./optional"

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