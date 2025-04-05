from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.permissions import AllowAny
from .models import DailyRecord, Transaction
from .serializers import UserSerializer, DailyRecordSerializer, TransactionSerializer
from django.contrib.auth import get_user_model

from django.db.models import Sum
from datetime import datetime
from rest_framework.decorators import action
from collections import defaultdict

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.pk})
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
    
# ViewSet cho CustomUser
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # For user logined

# ViewSet for DailyRecord
class DailyRecordViewSet(viewsets.ModelViewSet):
    queryset = DailyRecord.objects.all()
    serializer_class = DailyRecordSerializer
    permission_classes = [IsAuthenticated]  # For user logined

    def perform_create(self, serializer):
        # Assign current user to the daily record
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return DailyRecord.objects.filter(user=self.request.user)

# ViewSet for Transaction
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]  # For user logined

    def get_queryset(self):
        # Filter Transactions follow Daily Records of current user
        return Transaction.objects.filter(daily_record__user=self.request.user)

    @action(detail=False, methods=['get'], url_path='monthly')
    def monthly(self, request):
        month = request.query_params.get('month', datetime.now().month)
        year = request.query_params.get('year', datetime.now().year)

        queryset = self.get_queryset()

        total_expense = queryset.filter(
            type="expense",
            date__month=month,
            date__year=year
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_income = queryset.filter(
            type="income",
            date__month=month,
            date__year=year
        ).aggregate(total=Sum('amount'))['total'] or 0

        response_data = {"month": month, 
                         "year": year, 
                         "total_expense": total_expense,
                         "total_income": total_income,
                         "net_balance": total_income - total_expense}

        return Response(response_data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='daily-expenses')
    def daily_expenses(self, request):
        # Lấy tháng và năm từ query params
        month = request.query_params.get('month', datetime.now().month)
        year = request.query_params.get('year', datetime.now().year)

        # Lọc giao dịch theo tháng và năm dựa trên trường `date`
        transactions = self.get_queryset().filter(
            date__month=month,
            date__year=year
        ).values('date', 'type').annotate(total=Sum('amount'))

        # Tổ chức dữ liệu theo ngày
        daily_data = defaultdict(lambda: {'income': 0, 'expense': 0})
        for transaction in transactions:
            date = transaction['date']
            daily_data[date][transaction['type']] += transaction['total']

        # Chuyển đổi dữ liệu thành danh sách
        result = [
            {'date': date, 'income': data['income'], 'expense': data['expense']}
            for date, data in sorted(daily_data.items())
        ]

        return Response({"month": month, "year": year, "daily_expenses": result})
