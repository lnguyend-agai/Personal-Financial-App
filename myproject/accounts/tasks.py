from celery import shared_task
from django.core.mail import send_mail
from django.db.models import Sum
from datetime import datetime
from .models import Transaction
import logging

logger = logging.getLogger(__name__)
@shared_task
def send_monthly_report(user_email, user_id):
    try:
        now = datetime.now()
        month = now.month
        year = now.year

        logger.info(f"Preparing report for user {user_id} ({user_email})")

        total_income = Transaction.objects.filter(
            daily_record__user_id=user_id,
            type='income',
            date__month=month,
            date__year=year
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_expense = Transaction.objects.filter(
            daily_record__user_id=user_id,
            type='expense',
            date__month=month,
            date__year=year
        ).aggregate(total=Sum('amount'))['total'] or 0

        net_balance = total_income - total_expense

        subject = f"Monthly Financial Report - {now.strftime('%B %Y')}"
        message = (
            f"Hello,\n\n"
            f"Here is your financial report for {now.strftime('%B %Y')}:\n"
            f"- Total Income: {total_income} VND\n"
            f"- Total Expense: {total_expense} VND\n"
            f"- Net Balance: {net_balance} VND\n\n"
            f"Thank you for using our service!"
        )

        send_mail(
            subject,
            message,
            'noreply@financialapp.com',
            [user_email],
            fail_silently=False,
        )

        logger.info(f"Email sent successfully to {user_email}")

    except Exception as e:
        logger.error(f"Error sending monthly report to {user_email}: {e}", exc_info=True)
        raise e