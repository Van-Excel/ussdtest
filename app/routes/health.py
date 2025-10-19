from fastapi import APIRouter
from app.core.config import redis_client

router = APIRouter()

@router.get("/health")
def health_check():
    try:
        redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "redis": str(e)}
