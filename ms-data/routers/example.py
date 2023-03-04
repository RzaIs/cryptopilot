from fastapi import APIRouter

router: APIRouter = APIRouter(
  prefix = '/example',
  responses = { 404: { "description": "not found" } }
)

@router.get('/data')
async def get_example() -> dict[str, str]:
  return { "example" : "data" }