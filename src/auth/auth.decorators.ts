import { createParamDecorator, ExecutionContext } from "@nestjs/common"
import { Optional, some } from "src/helper/optional"

function factory<T>(data: Optional<string>, context: ExecutionContext): T {
  const request = context.switchToHttp().getRequest()
  if (some(data)) {
    return request.user[data]
  } else {
    return request.user
  }
}

export const GetUser = createParamDecorator(factory)