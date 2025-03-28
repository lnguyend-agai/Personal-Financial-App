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

        total_expense = self.get_queryset().filter(
            type="expense",
            created_at__month=month,
            created_at__year=year
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response({"month": month, "year": year, "total_expense": total_expense})
