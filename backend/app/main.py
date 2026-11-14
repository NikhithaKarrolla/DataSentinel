
from fastapi import FastAPI
from app.routes.datasets import router as dataset_router

app = FastAPI(
    title="DataSentinel API",
    description="AI-Powered Data Quality Intelligence Platform",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to DataSentinel!",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {"status": "Healthy"}


app.include_router(dataset_router)
