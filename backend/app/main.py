from app.orbital_api_client import OrbitalAPIClient
from app.usage_handler import UsageHandler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_client = OrbitalAPIClient()
usage_handler = UsageHandler(api_client=api_client)

@app.get("/")
def read_root():
    return {"message": "Hello, Orbital!"}

@app.get("/usage")
def get_usage() -> dict:
    usages = usage_handler.get_usages_for_current_period()
    return {"usage": [usage.model_dump() for usage in usages]}