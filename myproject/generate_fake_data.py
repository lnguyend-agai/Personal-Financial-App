import os
import django
import random
from datetime import datetime, timedelta
from faker import Faker
from django.contrib.auth.hashers import make_password
from tqdm import tqdm

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from accounts.models import CustomUser, DailyRecord, Transaction

fake = Faker()

def create_fake_users(num_users=1000):
    """Create fake users with default password"""
    users = []
    for i in tqdm(range(num_users), desc="Creating users"):
        username = f"customer{i+1}"
        email = fake.email()
        password = make_password('password123')  # Default password: password123
        user = CustomUser(
            username=username,
            email=email,
            password=password,
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        users.append(user)
    
    # Bulk create users
    CustomUser.objects.bulk_create(users)
    return CustomUser.objects.filter(username__startswith='customer')

def create_fake_daily_records(users, days_back=365):
    """Create daily records for each user"""
    daily_records = []
    for user in tqdm(users, desc="Creating daily records"):
        for i in range(days_back):
            date = datetime.now().date() - timedelta(days=i)
            # Generate reasonable random income and expense
            total_income = round(random.uniform(40, 100), 2)  # Income range: 40-100
            total_expense = round(random.uniform(30, 80), 2)  # Expense range: 30-80
            
            daily_record = DailyRecord(
                user=user,
                date=date,
                total_income=total_income,
                total_expense=total_expense
            )
            daily_records.append(daily_record)
    
    # Bulk create daily records
    DailyRecord.objects.bulk_create(daily_records)
    return DailyRecord.objects.filter(user__in=users)

def create_fake_transactions(daily_records):
    """Create transactions for each daily record"""
    transactions = []
    for daily_record in tqdm(daily_records, desc="Creating transactions"):
        # Create income transactions
        # 1. Salary (range: 30-60)
        salary_amount = round(random.uniform(30, 60), 2)
        transactions.append(Transaction(
            daily_record=daily_record,
            type='income',
            category='salary',
            amount=salary_amount,
            date=daily_record.date
        ))
        
        # 2. Coffee Sales (range: 10-40)
        coffee_amount = round(random.uniform(10, 40), 2)
        transactions.append(Transaction(
            daily_record=daily_record,
            type='income',
            category='coffeeSales',
            amount=coffee_amount,
            date=daily_record.date
        ))
        
        # Create expense transactions
        # 1. Transport (range: 15-30)
        transport_amount = round(random.uniform(15, 30), 2)
        transactions.append(Transaction(
            daily_record=daily_record,
            type='expense',
            category='transport',
            amount=transport_amount,
            date=daily_record.date
        ))
        
        # 2. Food (range: 15-50)
        food_amount = round(random.uniform(15, 50), 2)
        transactions.append(Transaction(
            daily_record=daily_record,
            type='expense',
            category='food',
            amount=food_amount,
            date=daily_record.date
        ))
    
    # Bulk create transactions
    Transaction.objects.bulk_create(transactions)

def main():
    print("Starting to generate fake data...")
    
    # Ask user if they want to delete existing data
    response = input("Do you want to delete existing data before creating new ones? (y/n): ")
    if response.lower() == 'y':
        print("Deleting existing data...")
        Transaction.objects.all().delete()
        DailyRecord.objects.all().delete()
        CustomUser.objects.exclude(username='123').delete()  # Keep the superuser
        print("Existing data deleted!")
    
    # Get user input for number of users and days
    num_users = int(input("Enter number of users to create (default 1000): ") or "1000")
    days_back = int(input("Enter number of days of history to create (default 365): ") or "365")
    
    # Create users
    print(f"\nCreating {num_users} users...")
    users = create_fake_users(num_users)
    print(f"Successfully created {len(users)} users!")
    
    # Create daily records
    print(f"\nCreating daily records for {days_back} days...")
    daily_records = create_fake_daily_records(users, days_back)
    print(f"Successfully created {len(daily_records)} daily records!")
    
    # Create transactions
    print("\nCreating transactions...")
    create_fake_transactions(daily_records)
    print("Successfully created all transactions!")
    
    print("\nFake data generation completed!")

if __name__ == "__main__":
    main() 