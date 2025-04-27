from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Thêm related_name để tránh xung đột
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Thêm related_name để tránh xung đột
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )

# DailyRecord Model
class DailyRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="daily_records")
    date = models.DateField()
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    class Meta:
        indexes = [
            models.Index(fields=['user', 'date']),  # Composite index for user's daily records
            models.Index(fields=['date']),  # Index for date-based queries
        ]

# Transaction Model
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    daily_record = models.ForeignKey(DailyRecord, on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=50)  # e.g., "food", "transport", "salary"
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.category} - {self.amount}"

    class Meta:
        indexes = [
            models.Index(fields=['daily_record', 'type']),  # Composite index for daily record transactions
            models.Index(fields=['type', 'category']),  # Index for type and category queries
            models.Index(fields=['date']),  # Index for date-based queries
        ]