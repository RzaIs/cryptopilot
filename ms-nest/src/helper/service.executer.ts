import { randomUUID } from "crypto"

export async function executeAsync<T>(promise: Promise<T>): Promise<T> {
  try {
    return await promise    
  } catch (error) {
    const uuid = randomUUID()
    if (error.response) {
      error.response.uuid = uuid
    } else {
      error.uuid = uuid
    }
    console.log(error)
    throw error
  }
}

export function execute<T>(action: () => T): T {
  try {
    return action()    
  } catch (error) {
    const uuid = randomUUID()
    if (error.response) {
      error.response.uuid = uuid
    } else {
      error.uuid = uuid
    }
    console.log(error)
    throw error
  }
}
