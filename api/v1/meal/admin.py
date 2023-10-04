from django.contrib import admin
from django import forms
from .models import Vendor, Menu, Meal, Review, CustomUser, MealReview


class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone_number',
        'email',
        'address',
    )


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'

    meals = forms.ModelMultipleChoiceField(
        queryset=Meal.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('meals', is_stacked=False),
        required=True
    )


class MenuAdmin(admin.ModelAdmin):
    form = MenuForm
    list_display = (
        'name',
        'description',
        'get_meals',
    )

    def get_meals(self, obj):
        meals = obj.meals.all()
        meal_names = [meal.name for meal in meals]
        return ', '.join(meal_names)

    get_meals.short_description = 'Meals'


class MealAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'vendor',
        'datetime',
        'cost',
        'is_lunch',
        'is_dinner',
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'rating',
        'comment',
    )


class ReviewMealAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'meal',
        'review',
    )


admin.site.register(Vendor, VendorAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(MealReview, ReviewMealAdmin)
