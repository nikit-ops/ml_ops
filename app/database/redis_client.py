import redis
from .config import get_settings

settings = get_settings()

# Configure Redis connection
redis_client = redis.StrictRedis(
    host="ml-task-redis",
    port=6379,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)
