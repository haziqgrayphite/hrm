from django.contrib import admin
from django import forms
from .models import BaseEvaluation, CustomUser, Parameter, ParameterRating, Evaluation, EvaluationScore


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
        'display_scores',
        'is_active',
        'is_evaluated',
    ]

    def display_scores(self, obj):
        evaluation_scores = obj.evaluation_score.all()
        return ', '.join([str(score) for score in evaluation_scores])

    display_scores.short_description = 'Scores'


class EvaluationScoreAdmin(admin.ModelAdmin):
    list_display = [
         'parameter',
         'parameter_rating'
    ]


admin.site.register(BaseEvaluation, BaseEvaluationAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(ParameterRating, ParameterRatingAdmin)
admin.site.register(EvaluationScore, EvaluationScoreAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
