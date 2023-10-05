from rest_framework import serializers
from .models import Vendor, Meal, Menu, Review, MealReview
from api.v1.accounts.serializers import CustomUserSerializer


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('name', 'phone_number', 'email', 'address')


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('vendor', 'name', 'description', 'cost', 'is_lunch', 'is_dinner')


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('name', 'description', 'meals')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('rating', 'comment')


class MealReviewSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    meal = MealSerializer()
    review = ReviewSerializer()

    class Meta:
        model = MealReview
        fields = ('user', 'meal', 'review')
