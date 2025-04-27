from django.test import TestCase
from django.utils import timezone
from ..models import CustomUser, DailyRecord, Transaction
from ..queries import DailyRecordQueries, TransactionQueries
from datetime import datetime, timedelta

class TestQueries(TestCase):
    def setUp(self):
        # Create test user
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test daily records
        today = timezone.now().date()
        self.daily_record = DailyRecord.objects.create(
            user=self.user,
            date=today,
            total_income=100.00,
            total_expense=50.00
        )
        
        # Create test transactions
        Transaction.objects.create(
            daily_record=self.daily_record,
            type='income',
            category='salary',
            amount=100.00,
            date=today
        )
        Transaction.objects.create(
            daily_record=self.daily_record,
            type='expense',
            category='food',
            amount=50.00,
            date=today
        )

    def test_get_user_daily_records(self):
        # Test getting user's daily records
        start_date = timezone.now().date() - timedelta(days=1)
        end_date = timezone.now().date() + timedelta(days=1)
        
        records = DailyRecordQueries.get_user_daily_records(
            self.user.id,
            start_date,
            end_date
        )
        
        self.assertEqual(records.count(), 1)
        self.assertEqual(records.first().user, self.user)

    def test_get_daily_records_by_date(self):
        # Test getting records by date
        records = DailyRecordQueries.get_daily_records_by_date(
            timezone.now().date()
        )
        
        self.assertEqual(records.count(), 1)
        self.assertEqual(records.first().date, timezone.now().date())

    def test_get_user_monthly_summary(self):
        # Test getting monthly summary
        summary = DailyRecordQueries.get_user_monthly_summary(
            self.user.id,
            timezone.now().year,
            timezone.now().month
        )
        
        self.assertEqual(summary['total_income'], 100.00)
        self.assertEqual(summary['total_expense'], 50.00)

    def test_get_daily_record_transactions(self):
        # Test getting transactions for a daily record
        transactions = TransactionQueries.get_daily_record_transactions(
            self.daily_record.id
        )
        
        self.assertEqual(transactions.count(), 2)

    def test_get_transactions_by_type_and_category(self):
        # Test getting transactions by type and category
        expenses = TransactionQueries.get_transactions_by_type_and_category(
            'expense',
            'food'
        )
        
        self.assertEqual(expenses.count(), 1)
        self.assertEqual(expenses.first().amount, 50.00)

    def test_get_transactions_by_date_range(self):
        # Test getting transactions by date range
        start_date = timezone.now().date() - timedelta(days=1)
        end_date = timezone.now().date() + timedelta(days=1)
        
        transactions = TransactionQueries.get_transactions_by_date_range(
            start_date,
            end_date
        )
        
        self.assertEqual(transactions.count(), 2)

    def test_get_user_transactions_summary(self):
        # Test getting user's transaction summary
        start_date = timezone.now().date() - timedelta(days=1)
        end_date = timezone.now().date() + timedelta(days=1)
        
        summary = TransactionQueries.get_user_transactions_summary(
            self.user.id,
            start_date,
            end_date
        )
        
        # Convert to list to make it easier to test
        summary_list = list(summary)
        
        self.assertEqual(len(summary_list), 2)  # Should have income and expense
        self.assertEqual(summary_list[0]['total_amount'], 100.00)  # Income
        self.assertEqual(summary_list[1]['total_amount'], 50.00)   # Expense 