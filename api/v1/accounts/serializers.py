from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        user = CustomUser(
            gender=validated_data['gender'],
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            is_staff=validated_data['is_staff'],
            is_active=validated_data['is_active']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



