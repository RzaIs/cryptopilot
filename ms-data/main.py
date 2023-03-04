from fastapi import FastAPI
from routers.example import router as example_router
from middleware.api_key_validator import api_key_validator

app: FastAPI = FastAPI()

app.middleware('http')(api_key_validator)

app.include_router(example_router)