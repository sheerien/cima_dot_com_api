# """
# Redis cache for fast repeated access.
# """

# import json
# import redis
# from app.settings import REDIS_HOST, REDIS_PORT, CACHE_TTL

# redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


# def get_cached(work_id: str):
#     """Retrieve cached data from Redis if exists."""
#     value = redis_client.get(work_id)
#     return json.loads(value) if value else None


# def set_cache(work_id: str, data: dict):
#     """Set cache with TTL in Redis."""
#     redis_client.setex(work_id, CACHE_TTL, json.dumps(data, ensure_ascii=False))




"""
Temporary in-memory cache for development.
Use real Redis later for production.
"""

_cache = {}  # In-memory dictionary for caching


def get_cached(work_id: str):
    """
    Retrieve cached data if exists.
    This is a dummy cache for development purposes.
    """
    return _cache.get(work_id)


def set_cache(work_id: str, data: dict):
    """
    Store data in dummy cache.
    """
    _cache[work_id] = data

