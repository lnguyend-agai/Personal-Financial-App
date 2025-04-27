from django.db.models import Sum, Count, Avg, F, Q
from django.db import connection
from .models import DailyRecord, Transaction, CustomUser
from datetime import datetime, timedelta, date
import logging

logger = logging.getLogger(__name__)

class DailyRecordQueries:
    @staticmethod
    def get_user_daily_records(user_id: int, start_date: date, end_date: date):
        """
        Get daily records for a specific user within a date range
        Using index: (user, date)
        """
        return DailyRecord.objects.filter(
            user_id=user_id,
            date__gte=start_date,
            date__lte=end_date
        ).select_related('user')

    @staticmethod
    def get_daily_records_by_date(date: date):
        """
        Get all daily records for a specific date
        Using index: (date)
        """
        return DailyRecord.objects.filter(date=date)

    @staticmethod
    def get_user_monthly_summary(user_id: int, year: int, month: int):
        """
        Get monthly summary for a user
        Using index: (user, date)
        """
        return DailyRecord.objects.filter(
            user_id=user_id,
            date__year=year,
            date__month=month
        ).aggregate(
            total_income=Sum('total_income'),
            total_expense=Sum('total_expense')
        )

class TransactionQueries:
    @staticmethod
    def get_daily_record_transactions(daily_record_id: int, transaction_type: str = None):
        """
        Get transactions for a daily record, optionally filtered by type
        Using index: (daily_record, type)
        """
        query = Transaction.objects.filter(daily_record_id=daily_record_id)
        if transaction_type:
            query = query.filter(type=transaction_type)
        return query

    @staticmethod
    def get_transactions_by_type_and_category(transaction_type: str, category: str):
        """
        Get transactions by type and category
        Using index: (type, category)
        """
        return Transaction.objects.filter(
            type=transaction_type,
            category__iexact=category
        ).select_related('daily_record', 'daily_record__user')

    @staticmethod
    def get_transactions_by_date_range(start_date: date, end_date: date):
        """
        Get transactions within a date range
        Using index: (date)
        """
        return Transaction.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).select_related('daily_record', 'daily_record__user')

    @staticmethod
    def get_user_transactions_summary(user_id: int, start_date: date, end_date: date):
        """
        Get detailed transaction summary for a user
        Using multiple indexes
        """
        # Get daily records first (using user, date index)
        daily_records = DailyRecord.objects.filter(
            user_id=user_id,
            date__gte=start_date,
            date__lte=end_date
        ).values_list('id', flat=True)

        # Then get transactions (using daily_record, type index)
        return Transaction.objects.filter(
            daily_record_id__in=daily_records
        ).values('type', 'category').annotate(
            total_amount=Sum('amount'),
            transaction_count=Count('id')
        ).order_by('-total_amount')

def explain_query(query):
    """
    Helper function to explain the query execution plan
    """
    with connection.cursor() as cursor:
        sql, params = query.query.sql_with_params()
        cursor.execute("EXPLAIN ANALYZE " + sql, params)
        return cursor.fetchall()

# Example usage:
if __name__ == "__main__":
    # Example 1: Get user's daily records for last month
    last_month = datetime.now() - timedelta(days=30)
    user_records = DailyRecordQueries.get_user_daily_records(
        user_id=1,
        start_date=last_month.date(),
        end_date=datetime.now().date()
    )
    logger.info(f"Found {user_records.count()} daily records")

    # Example 2: Get all food expenses
    food_expenses = TransactionQueries.get_transactions_by_type_and_category(
        transaction_type='expense',
        category='food'
    )
    logger.info(f"Found {food_expenses.count()} food expenses")

    # Example 3: Get monthly summary
    monthly_summary = DailyRecordQueries.get_user_monthly_summary(
        user_id=1,
        year=datetime.now().year,
        month=datetime.now().month
    )
    logger.info(f"Monthly summary: {monthly_summary}")

    # Example 4: Get detailed transaction summary
    transaction_summary = TransactionQueries.get_user_transactions_summary(
        user_id=1,
        start_date=last_month.date(),
        end_date=datetime.now().date()
    )
    logger.info(f"Transaction summary: {list(transaction_summary)}") 