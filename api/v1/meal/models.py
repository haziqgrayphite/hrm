from django.db import models
from django.utils import timezone
from api.v1.accounts.models import CustomUser


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    meals = models.ManyToManyField('Meal', related_name='menus')

    name = models.CharField(max_length=255)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Meal(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True, related_name="meals")

    name = models.CharField(max_length=255)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    is_lunch = models.BooleanField(default=True)
    is_dinner = models.BooleanField(default=False)

    datetime = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review - Rating: {self.rating}"


class MealReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='meal_users')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='meal_meals')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='meal_reviews')

    def __str__(self):
        return f"MealReview by {self.user} for {self.meal}"

    class Meta:
        unique_together = ('user', 'meal')
