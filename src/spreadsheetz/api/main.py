"""
Main API file.
"""
from fastapi import FastAPI
from spreadsheetz.api.endpoints import predict
from spreadsheetz.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(predict.router, prefix="/predict", tags=["predict"])

@app.get("/")
def root():
    """
    Root endpoint.
    """
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}
