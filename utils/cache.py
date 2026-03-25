"""Cache utilities - Redis integration for caching"""

import redis
import json
import logging
from typing import Any, Optional
from datetime import timedelta

logger = logging.getLogger(__name__)

# Redis client (connect to local Redis)
try:
    redis_client = redis.Redis(
        host='localhost',
        port=6379,
        db=0,
        decode_responses=True
    )
    # Test connection
    redis_client.ping()
    logger.info("✅ Redis connected successfully")
except Exception as e:
    logger.warning(f"⚠️ Redis not available: {e}")
    redis_client = None  # Fallback to None


def cache_get(key: str) -> Optional[Any]:
    """Get value from cache"""
    try:
        if redis_client is None:
            return None
        
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        logger.warning(f"Cache get error: {e}")
        return None


def cache_set(key: str, value: Any, ttl: int = 3600) -> bool:
    """Set value in cache with TTL"""
    try:
        if redis_client is None:
            return False
        
        redis_client.setex(
            key,
            timedelta(seconds=ttl),
            json.dumps(value)
        )
        return True
    except Exception as e:
        logger.warning(f"Cache set error: {e}")
        return False


def cache_delete(key: str) -> bool:
    """Delete value from cache"""
    try:
        if redis_client is None:
            return False
        
        redis_client.delete(key)
        return True
    except Exception as e:
        logger.warning(f"Cache delete error: {e}")
        return False


def cache_exists(key: str) -> bool:
    """Check if key exists in cache"""
    try:
        if redis_client is None:
            return False
        
        return redis_client.exists(key) > 0
    except Exception as e:
        logger.warning(f"Cache exists error: {e}")
        return False


def cache_clear_pattern(pattern: str) -> int:
    """Clear all keys matching pattern"""
    try:
        if redis_client is None:
            return 0
        
        keys = redis_client.keys(pattern)
        if keys:
            return redis_client.delete(*keys)
        return 0
    except Exception as e:
        logger.warning(f"Cache clear error: {e}")
        return 0
