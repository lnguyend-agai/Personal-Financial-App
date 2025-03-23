from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, DailyRecord, Transaction

# Đăng ký CustomUser với UserAdmin
admin.site.register(CustomUser, UserAdmin)

# Đăng ký DailyRecord
@admin.register(DailyRecord)
class DailyRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'total_income', 'total_expense', 'created_at', 'updated_at')
    list_filter = ('date', 'user')
    search_fields = ('user__username', 'date')

# Đăng ký Transaction
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('daily_record', 'type', 'category', 'amount', 'created_at')
    list_filter = ('type', 'category', 'daily_record__user')
    search_fields = ('daily_record__user__username', 'category')