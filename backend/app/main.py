from fastapi import FastAPI

app = FastAPI(
    title="DataSentinel API",
    description="AI-Powered Data Quality Intelligence Platform",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to DataSentinel!",
        "status": "Running",
        "project": "AI Data Quality Intelligence Platform"
    }


@app.get("/health")
def health_check():
    return {
        "status": "Healthy",
        "service": "DataSentinel Backend"
    }