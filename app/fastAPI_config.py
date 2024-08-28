from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from app import consts

# Enable CORS based on environment
if consts.ENV == "PROD":
    allow_origins = ["https://front-tikroast.vercel.app"]
else:
    allow_origins = [
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:3000",
        "https://front-tikroast.vercel.app",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
