from django.contrib import admin
from django import forms
from django.db import transaction
from .models import CustomUser, BaseEvaluation


class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'gender',
        'role',
        'date_joined',
        'created_at',
        'updated_at'
    ]


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = BaseEvaluation
        fields = '__all__'

    evaluator = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('evaluator', is_stacked=False),
        required=True
    )
    to_be_evaluated = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('evaluatee', is_stacked=False),
        required=True
    )


class EvaluationAdmin(admin.ModelAdmin):
    form = EvaluationForm
    exclude = ('is_completed', 'overall_comments', 'ratings')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(BaseEvaluation, EvaluationAdmin)
