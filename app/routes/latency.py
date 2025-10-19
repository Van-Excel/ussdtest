from fastapi import APIRouter
import time
from app.core.config import redis_client
from app.core.resilience import with_redis_resilience
from app.core.metrics import REQUEST_COUNT, REQUEST_LATENCY

router = APIRouter()

@router.get("/redis-latency")
@with_redis_resilience
def redis_latency_test(iterations: int = 100):
    REQUEST_COUNT.labels(endpoint="/redis-latency").inc()

    key, value = "latency:test", "ping"
    times = []

    for _ in range(iterations):
        start = time.perf_counter()
        redis_client.set(key, value)
        redis_client.get(key)
        duration_ms = (time.perf_counter() - start) * 1000
        REQUEST_LATENCY.observe(duration_ms)
        times.append(duration_ms)

    avg_latency = sum(times) / len(times)
    return {
        "iterations": iterations,
        "average_latency_ms": round(avg_latency, 3),
        "min_latency_ms": round(min(times), 3),
        "max_latency_ms": round(max(times), 3),
    }
