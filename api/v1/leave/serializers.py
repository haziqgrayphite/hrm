from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import LeaveRequest, LeaveRequestTL, LeaveRequestHR, LeaveBalance
User = get_user_model()


class LeaveRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = LeaveRequest
        fields = '__all__'


class LeaveRequestTLSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequestTL
        fields = '__all__'


class LeaveRequestTLLSerializer(serializers.ModelSerializer):
    leave_request = LeaveRequestSerializer()
    class Meta:
        model = LeaveRequestTL
        fields = '__all__'


class LeaveRequestHRSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequestHR
        fields = '__all__'


class LeaveRequestHRRSerializer(serializers.ModelSerializer):
    leave_request = LeaveRequestSerializer()

    class Meta:
        model = LeaveRequestHR
        fields = '__all__'


class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveBalance
        fields = '__all__'
