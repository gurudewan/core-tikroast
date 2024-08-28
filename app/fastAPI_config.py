from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from app import consts

""" # Enable CORS based on environment
if consts.ENV == "PROD":
    allow_origins=["*"],  # Allow all origins
else:
    allow_origins=["*"],  # Allow all origins


app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) """
