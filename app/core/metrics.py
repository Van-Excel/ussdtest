from prometheus_client import Counter, Histogram

# Count total requests (by endpoint)
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests handled by the API",
    ["endpoint"]
)

# Measure Redis operation latency
REQUEST_LATENCY = Histogram(
    "redis_request_latency_ms",
    "Latency of Redis operations (set/get) in milliseconds"
)

# Count Redis connection errors
REDIS_ERRORS = Counter(
    "redis_connection_errors_total",
    "Number of Redis connection failures"
)
