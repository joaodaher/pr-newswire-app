import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.articles import endpoints

app = FastAPI(
    title="Wire Scout API",
    description="API for PR Newswire content",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"message": "Welcome to Wire Scout API!"}


app.include_router(endpoints.router)


# Default to development server origin if not set
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:5173")
origins = [origin.strip() for origin in cors_origins_str.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
