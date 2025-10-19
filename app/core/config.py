import os
import redis.sentinel

# Sentinel configuration
sentinel_hosts = [
    tuple(host.strip().split(":"))
    for host in os.getenv("REDIS_SENTINEL_HOSTS", "redis-sentinel1:26379").split(",")
]
master_name = os.getenv("REDIS_MASTER_NAME", "mymaster")

# Connect via Sentinel
sentinel = redis.sentinel.Sentinel(sentinel_hosts, socket_timeout=0.5)
redis_client = sentinel.master_for(master_name, socket_timeout=0.5)

