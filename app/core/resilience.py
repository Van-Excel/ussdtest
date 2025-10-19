import time
import redis
from functools import wraps
from app.core.metrics import REDIS_ERRORS

MAX_FAILURES = 3
failure_count = 0
circuit_open_until = 0

def with_redis_resilience(func):
    """
    Decorator that adds retry and circuit breaker logic
    for Redis operations.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        global failure_count, circuit_open_until
        now = time.time()

        # Circuit open — temporarily disable Redis operations
        if now < circuit_open_until:
            return {"error": "Redis temporarily disabled (circuit open)"}

        try:
            return func(*args, **kwargs)
        except redis.exceptions.ConnectionError:
            REDIS_ERRORS.inc()
            failure_count += 1
            if failure_count >= MAX_FAILURES:
                circuit_open_until = now + 30  # open for 30s
                failure_count = 0
            return {"error": "Redis connection failed"}
    return wrapper
