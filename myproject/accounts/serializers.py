from rest_framework import serializers
from .models import DailyRecord, Transaction
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    
class DailyRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Hiển thị username thay vì user_id

    class Meta:
        model = DailyRecord
        fields = '__all__'  # Bao gồm tất cả các trường trong model
        
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'