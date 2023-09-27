from django.contrib import admin
from django import forms
from .models import BaseEvaluation, CustomUser, Parameter, ParameterRating, Evaluation


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = BaseEvaluation
        fields = '__all__'

    evaluators = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('evaluator', is_stacked=False),
        required=True
    )
    evaluatees = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('evaluatee', is_stacked=False),
        required=True
    )

    parameters = forms.ModelMultipleChoiceField(
        queryset=Parameter.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('parameter', is_stacked=False),
        required=True
    )


class BaseEvaluationAdmin(admin.ModelAdmin):
    form = EvaluationForm
    exclude = ('is_completed', 'overall_comments', 'ratings', 'valid_until')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class ParameterAdmin(admin.ModelAdmin):
    list_display = [
        'is_active',
        'name',
        'description',
    ]


class ParameterRatingAdmin(admin.ModelAdmin):
    list_display = [
        'is_active',
        'name',
        'score'
    ]


class EvaluationAdmin(admin.ModelAdmin):
    list_display = [
        'evaluator',
        'evaluatee',
        'display_parameters',
        'is_active',
        'is_evaluated',
    ]

    def display_parameters(self, obj):
        parameters = obj.parameters.all()
        return ', '.join([str(parameter.name) for parameter in parameters])

    display_parameters.short_description = 'Parameters'


admin.site.register(BaseEvaluation, BaseEvaluationAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(ParameterRating, ParameterRatingAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
