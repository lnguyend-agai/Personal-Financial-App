from django.core.cache import cache
from django.conf import settings
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)

class RedisCacheService:
    """
    Service class to handle Redis caching following the flow:
    1. Check Cache
    2. Cache Hit -> Return Cached Data
    3. Cache Miss -> Query Database -> Store in Cache -> Return Data
    4. Transaction Change -> Invalidate Cache
    """
    
    @staticmethod
    def get_cache(key: str) -> Optional[Any]:
        """
        Check and retrieve data from cache
        Returns: Data if cache hit, None if cache miss
        """
        try:
            cached_data = cache.get(key)
            if cached_data is not None:
                logger.info(f"Cache hit for key: {key}")
                return cached_data
            logger.info(f"Cache miss for key: {key}")
            return None
        except Exception as e:
            logger.error(f"Error getting cache for key {key}: {str(e)}")
            return None

    @staticmethod
    def set_cache(key: str, data: Any, timeout: int = None) -> bool:
        """
        Store data in cache
        Args:
            key: Cache key
            data: Data to be cached
            timeout: TTL in seconds, defaults to settings.CACHE_TTL
        Returns: True if successful, False if failed
        """
        try:
            timeout = timeout or getattr(settings, 'CACHE_TTL', 3600)
            cache.set(key, data, timeout)
            logger.info(f"Data stored in cache for key: {key}")
            return True
        except Exception as e:
            logger.error(f"Error setting cache for key {key}: {str(e)}")
            return False

    @staticmethod
    def invalidate_cache(key: str) -> bool:
        """
        Delete cache when data changes
        Returns: True if successful, False if failed
        """
        try:
            cache.delete(key)
            logger.info(f"Cache invalidated for key: {key}")
            return True
        except Exception as e:
            logger.error(f"Error invalidating cache for key {key}: {str(e)}")
            return False

    @staticmethod
    def invalidate_pattern(pattern: str) -> bool:
        """
        Delete all cache keys matching the pattern
        Example: invalidate_pattern("user:123:*") will delete all cache for user 123
        Returns: True if successful, False if failed
        """
        try:
            keys = cache.keys(pattern)
            if keys:
                cache.delete_many(keys)
                logger.info(f"Cache invalidated for pattern: {pattern}")
            return True
        except Exception as e:
            logger.error(f"Error invalidating cache pattern {pattern}: {str(e)}")
            return False 