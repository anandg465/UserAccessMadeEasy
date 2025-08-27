import logging

logging.basicConfig(level=logging.INFO)
from fastapi import FastAPI
from app import api

app = FastAPI()
app.include_router(api.router)


@app.get("/")
def read_root():
    return {"message": "User Access Management Backend is running."}
