from fastapi import FastAPI
from app.routes import health, latency, metrics

app = FastAPI(title="FastAPI + Redis Latency Service")

# Register routers
app.include_router(health.router)
app.include_router(latency.router)
app.include_router(metrics.router)

@app.get("/")
def root():
    return {"message": "FastAPI + Redis Latency Benchmark Service"}
