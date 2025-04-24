from django.urls import path, include
from .views import RegisterView, LoginView, UserViewSet, DailyRecordViewSet, TransactionViewSet, DashboardView, SystemStatsView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'daily-records', DailyRecordViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('system-stats/', SystemStatsView.as_view(), name='system-stats'),
]