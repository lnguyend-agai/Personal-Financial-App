import os
import sys
import django
from datetime import datetime, timedelta, date
import logging

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from accounts.models import CustomUser, DailyRecord, Transaction
from accounts.queries import DailyRecordQueries, TransactionQueries, explain_query

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_query_performance(query, description):
    """
    Analyze query performance and log results
    """
    logger.info(f"\n=== Analyzing Query: {description} ===")
    
    try:
        # Get query plan
        plan = explain_query(query)
        logger.info("Query Plan:")
        for line in plan:
            logger.info(line[0])
        
        # Execute query and measure time
        start_time = datetime.now()
        result = list(query)
        end_time = datetime.now()
        
        logger.info(f"Query returned {len(result)} results")
        logger.info(f"Execution time: {(end_time - start_time).total_seconds():.4f} seconds")
        
        return result
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        return None

def main():
    # Get a test user with data
    user = CustomUser.objects.get(id=2468)  # Using user with known data
    logger.info(f"Using user: {user.username} (ID: {user.id})")

    # Set date range for analysis
    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    # 1. Analyze DailyRecord queries
    logger.info("\n=== Analyzing DailyRecord Queries ===")
    
    # Get user's daily records
    daily_records_query = DailyRecordQueries.get_user_daily_records(
        user.id,
        start_date,
        end_date
    )
    analyze_query_performance(
        daily_records_query,
        "Get user's daily records for last 30 days"
    )

    # Get monthly summary
    monthly_summary = DailyRecordQueries.get_user_monthly_summary(
        user.id,
        end_date.year,
        end_date.month
    )
    logger.info(f"\nMonthly Summary: {monthly_summary}")

    # 2. Analyze Transaction queries
    logger.info("\n=== Analyzing Transaction Queries ===")
    
    # Get transactions by type and category
    food_expenses_query = TransactionQueries.get_transactions_by_type_and_category(
        'expense',
        'food'
    )
    analyze_query_performance(
        food_expenses_query,
        "Get all food expenses"
    )

    # Get user's transaction summary
    transaction_summary_query = TransactionQueries.get_user_transactions_summary(
        user.id,
        start_date,
        end_date
    )
    analyze_query_performance(
        transaction_summary_query,
        "Get user's transaction summary"
    )

    # 3. Print database statistics
    logger.info("\n=== Database Statistics ===")
    logger.info(f"Total Users: {CustomUser.objects.count()}")
    logger.info(f"Total Daily Records: {DailyRecord.objects.count()}")
    logger.info(f"Total Transactions: {Transaction.objects.count()}")

if __name__ == "__main__":
    main() 