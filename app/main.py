import os
from fastapi import FastAPI

app = FastAPI(title="Lab 5 Jenkins CI/CD App")

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEPLOY_ENV = os.getenv("DEPLOY_ENV", "local")


@app.get("/")
def read_root():
    return {
        "service": "Jenkins CI/CD Pipeline Demo",
        "version": APP_VERSION,
        "environment": DEPLOY_ENV,
        "status": "operational"
    }


@app.get("/health")
def health():
    return {"status": "UP", "environment": DEPLOY_ENV}
