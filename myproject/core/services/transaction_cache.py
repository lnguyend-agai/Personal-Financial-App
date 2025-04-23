from django.db.models import Sum
from accounts.models import Transaction, DailyRecord
from core.services.redis_cache import RedisCacheService
import logging

logger = logging.getLogger(__name__)

class TransactionCacheService:
    """Service class to handle Transaction data caching"""

    # Cache key patterns
    SYSTEM_TOTAL_INCOME_KEY = "system:totals:income"
    SYSTEM_TOTAL_EXPENSE_KEY = "system:totals:expense"
    USER_TOTAL_PATTERN = "user:{user_id}:totals:{type}"  # type: income/expense

    @classmethod
    def get_user_total_key(cls, user_id: int, type: str) -> str:
        """Generate cache key for user total"""
        return cls.USER_TOTAL_PATTERN.format(user_id=user_id, type=type)

    @classmethod
    def get_system_totals(cls):
        """
        Get total income and expense for the entire system
        Flow: Check Cache -> Cache Hit/Miss -> Query DB if needed -> Return Data
        """
        # Check cache for both income and expense
        cached_income = RedisCacheService.get_cache(cls.SYSTEM_TOTAL_INCOME_KEY)
        cached_expense = RedisCacheService.get_cache(cls.SYSTEM_TOTAL_EXPENSE_KEY)

        # If we have all cached data
        if cached_income is not None and cached_expense is not None:
            return {
                'total_income': cached_income,
                'total_expense': cached_expense
            }

        # Cache miss -> Query from database
        total_income = Transaction.objects.filter(type='income').aggregate(
            total=Sum('amount'))['total'] or 0
        total_expense = Transaction.objects.filter(type='expense').aggregate(
            total=Sum('amount'))['total'] or 0

        # Store in cache
        RedisCacheService.set_cache(cls.SYSTEM_TOTAL_INCOME_KEY, total_income)
        RedisCacheService.set_cache(cls.SYSTEM_TOTAL_EXPENSE_KEY, total_expense)

        return {
            'total_income': total_income,
            'total_expense': total_expense
        }

    @classmethod
    def get_user_totals(cls, user_id: int):
        """
        Get total income and expense for a specific user
        Flow: Check Cache -> Cache Hit/Miss -> Query DB if needed -> Return Data
        """
        # Generate cache keys
        income_key = cls.get_user_total_key(user_id, 'income')
        expense_key = cls.get_user_total_key(user_id, 'expense')

        # Check cache
        cached_income = RedisCacheService.get_cache(income_key)
        cached_expense = RedisCacheService.get_cache(expense_key)

        # If we have all cached data
        if cached_income is not None and cached_expense is not None:
            return {
                'total_income': cached_income,
                'total_expense': cached_expense
            }

        # Cache miss -> Query from database
        # Update query to use daily_record relationship
        daily_records = DailyRecord.objects.filter(user_id=user_id)
        total_income = Transaction.objects.filter(
            daily_record__in=daily_records,
            type='income'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        total_expense = Transaction.objects.filter(
            daily_record__in=daily_records,
            type='expense'
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Store in cache
        RedisCacheService.set_cache(income_key, total_income)
        RedisCacheService.set_cache(expense_key, total_expense)

        return {
            'total_income': total_income,
            'total_expense': total_expense
        }

    @classmethod
    def invalidate_user_cache(cls, user_id: int):
        """Invalidate user's cache when transaction changes"""
        pattern = f"user:{user_id}:totals:*"
        RedisCacheService.invalidate_pattern(pattern)

    @classmethod
    def invalidate_system_cache(cls):
        """Invalidate system totals cache"""
        RedisCacheService.invalidate_cache(cls.SYSTEM_TOTAL_INCOME_KEY)
        RedisCacheService.invalidate_cache(cls.SYSTEM_TOTAL_EXPENSE_KEY)

    @classmethod
    def invalidate_all_cache(cls, user_id: int = None):
        """Invalidate all related cache when transaction changes"""
        # Always invalidate system cache
        cls.invalidate_system_cache()
        
        # Invalidate user cache if user_id is provided
        if user_id:
            cls.invalidate_user_cache(user_id) 