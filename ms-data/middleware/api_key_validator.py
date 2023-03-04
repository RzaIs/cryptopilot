import os
from fastapi import Request, Response
from typing import Callable, Awaitable

api_key: str | None = os.environ.get('BRIDGE_SECRET')

if (api_key is None):
  print('BRIDGE_SECRET missing')
  exit(1)


async def api_key_validator(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
  
  if request.headers.get('BRIDGE_SECRET') != api_key:
    return Response(
      content = 'invalid API Key',
      status_code = 401,
      media_type = 'application/json'
    )
  
  return await call_next(request)