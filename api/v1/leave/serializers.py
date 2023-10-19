from rest_framework import serializers
from .models import LeaveRequest, LeaveRequestTL, LeaveRequestHR


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'


class LeaveRequestTLSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequestTL
        fields = '__all__'


class LeaveRequestHRSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequestHR
        fields = '__all__'
