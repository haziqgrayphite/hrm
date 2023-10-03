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


# Meal Model
class Meal(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True, related_name="meals")
    attendees = models.ManyToManyField(CustomUser, related_name="meals_attending")

    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default="15:00")
    employee_wants_food = models.BooleanField(default=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="reviews")
    attendee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews_given")

    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rating for {self.meal} by {self.attendee}"
