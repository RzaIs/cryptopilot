from fastapi import FastAPI
from routers.ml import router as ml_router
from middleware.api_key_validator import api_key_validator

app: FastAPI = FastAPI()

app.middleware('http')(api_key_validator)

app.include_router(ml_router)