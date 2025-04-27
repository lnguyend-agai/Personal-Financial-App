import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.db.models import Q, Count
from accounts.models import CustomUser  # Using our CustomUser model
from datetime import datetime

def run_query_examples():
    """
    Examples of different types of Django ORM queries
    """
    # 1. GET - Get exactly one record
    try:
        user = CustomUser.objects.get(username='customer122')
        print(f"[GET] Username: {user.username}, Email: {user.email}")
    except CustomUser.DoesNotExist:
        print("[GET] User not found.")
    except CustomUser.MultipleObjectsReturned:
        print("[GET] Multiple users found.")

    # 2. FILTER - Get multiple records
    users = CustomUser.objects.filter(email__icontains='gmail.com')
    print(f"[FILTER] Found {users.count()} users with Gmail.")

    # 3. EXISTS - Check if record exists
    exists = CustomUser.objects.filter(username='test_user').exists()
    print(f"[EXISTS] User 'test_user' exists: {exists}")

    # 4. VALUES - Get list of dictionaries
    user_values = CustomUser.objects.filter(username__startswith='test').values('id', 'email')
    print(f"[VALUES] Users: {list(user_values)}")

    # 5. VALUES_LIST - Get list of tuples
    email_list = CustomUser.objects.filter(username__startswith='test').values_list('email', flat=True)
    print(f"[VALUES_LIST] Emails: {list(email_list)}")

    # 6. ONLY - Load only specific fields
    users_only = CustomUser.objects.only('username')
    for user in users_only[:5]:
        print(f"[ONLY] Username: {user.username}")

    # 7. DEFER - Don't load specific fields
    users_defer = CustomUser.objects.defer('password')
    for user in users_defer[:5]:
        print(f"[DEFER] Email: {user.email}")

    # 8. ORDER_BY - Sort by date
    users_ordered = CustomUser.objects.order_by('-date_joined')
    for user in users_ordered[:5]:
        print(f"[ORDER_BY] Joined at: {user.date_joined}, Username: {user.username}")

    # 9. AGGREGATE - Count users
    user_count = CustomUser.objects.aggregate(total=Count('id'))
    print(f"[AGGREGATE] Total users: {user_count['total']}")

    # 10. RAW - Raw SQL query
    users_raw = CustomUser.objects.raw('SELECT * FROM accounts_customuser WHERE email LIKE %s', ['%@gmail.com'])
    for user in users_raw:
        print(f"[RAW] Username: {user.username}, Email: {user.email}")

    # 11. Q Object - Complex queries
    users_q = CustomUser.objects.filter(
        Q(username__icontains='test') | Q(email__icontains='example.com')
    )
    print(f"[Q OBJECT] Found {users_q.count()} users with 'test' in username or 'example.com' in email.")

if __name__ == "__main__":
    run_query_examples() 