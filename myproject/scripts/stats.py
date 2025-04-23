import os
import sys
import django
from datetime import datetime, timedelta
from django.db.models import Count, Sum
from django.db import connection

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from accounts.models import CustomUser, DailyRecord, Transaction

def get_database_stats():
    """Get database statistics"""
    print("\n=== Database Statistics ===")
    
    # Total Users
    total_users = CustomUser.objects.count()
    print(f"Total Users: {total_users:,}")
    
    # Total Daily Records
    total_daily_records = DailyRecord.objects.count()
    print(f"Total Daily Records: {total_daily_records:,}")
    
    # Total Transactions
    total_transactions = Transaction.objects.count()
    print(f"Total Transactions: {total_transactions:,}")
    
    # Average transactions per user
    avg_transactions = total_transactions / total_users if total_users > 0 else 0
    print(f"Average Transactions per User: {avg_transactions:,.2f}")
    
    # Total Income and Expense
    total_income = Transaction.objects.filter(type='income').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    total_expense = Transaction.objects.filter(type='expense').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    print(f"\nTotal Income: ${total_income:,.2f}")
    print(f"Total Expense: ${total_expense:,.2f}")
    print(f"Net Balance: ${(total_income - total_expense):,.2f}")
    
    # Transactions by Category
    print("\nTransactions by Category:")
    category_stats = Transaction.objects.values('category').annotate(
        count=Count('id'),
        total=Sum('amount')
    ).order_by('-count')
    
    for stat in category_stats:
        print(f"{stat['category']}: {stat['count']:,} transactions, Total: ${stat['total']:,.2f}")
    
    # Database Size
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT pg_size_pretty(pg_database_size(current_database()));
        """)
        db_size = cursor.fetchone()[0]
        print(f"\nDatabase Size: {db_size}")

if __name__ == "__main__":
    get_database_stats() 