"""
Settings module for configuration management.
Loads environment variables and default values.
"""

import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://elcinema.com/work/")
AGENTQL_API_KEY = os.getenv("AGENTQL_API_KEY")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CACHE_TTL = int(os.getenv("CACHE_TTL", 86400))

if not AGENTQL_API_KEY:
    raise RuntimeError("AGENTQL_API_KEY is not set in .env")
