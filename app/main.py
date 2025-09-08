import time
import redis
from fastapi import FastAPI

app = FastAPI()

# Direct connection to Redis master (later we’ll switch to Sentinel)
redis_client = redis.Redis(host="redis-master", port=6379, db=0)

@app.get("/")
def read_root():
    return {"message": "FastAPI + Redis Latency Test"}

@app.get("/redis-latency")
def redis_latency_test():
    key = "latency:test"
    value = "ping"
    iterations = 100
    times = []

    for _ in range(iterations):
        start = time.perf_counter()
        redis_client.set(key, value)
        redis_client.get(key)
        end = time.perf_counter()
        times.append((end - start) * 1000)

    avg_latency = sum(times) / len(times)
    return {
        "iterations": iterations,
        "average_latency_ms": round(avg_latency, 3),
        "min_latency_ms": round(min(times), 3),
        "max_latency_ms": round(max(times), 3),
    }


@app.get("/redis-write-latency")
def redis_write_latency_test(iterations: int = 1000):
    """
    Test Redis latency for SET operations only.
    """
    key_prefix = "latency:write"
    value = "x" * 100  # 100-byte payload to simulate a small write
    times = []

    for i in range(iterations):
        key = f"{key_prefix}:{i}"
        start = time.perf_counter()
        redis_client.set(key, value)
        end = time.perf_counter()
        times.append((end - start) * 1000)  # ms

    avg_latency = sum(times) / len(times)
    return {
        "iterations": iterations,
        "average_write_latency_ms": round(avg_latency, 3),
        "min_write_latency_ms": round(min(times), 3),
        "max_write_latency_ms": round(max(times), 3),
    }
