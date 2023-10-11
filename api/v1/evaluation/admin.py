from django.contrib import admin
from django import forms
from django.db.models import Q
from django.db.models import Avg
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
    list_display = [
        'get_evaluators',
        'get_evaluatees',
        'get_parameters',
        'valid_from',
        'valid_until',
        'comment',
        'expiry_days',
        'is_active',
        'is_expired',
        'is_completed',
        'is_expirable'
        ]
    exclude = ('is_completed', 'overall_comments', 'ratings', 'valid_until')

    def get_parameters(self, obj):
        parameters = obj.parameters.all()
        parameter_names = [parameter.name for parameter in parameters]
        return parameter_names

    get_parameters.short_description = 'Parameters'

    def get_evaluators(self, obj):
        evaluators = obj.evaluators.all()
        return [evaluator.username for evaluator in evaluators]

    get_evaluators.short_description = 'Evaluators'

    def get_evaluatees(self, obj):
        evaluatees = obj.evaluatees.all()
        return [evaluatee.username for evaluatee in evaluatees]

    get_evaluatees.short_description = 'Evaluatees'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


class ParameterAdmin(admin.ModelAdmin):
    list_display = [
        'is_active',
        'name',
        'description',
        'comments'
    ]


class ParameterRatingAdmin(admin.ModelAdmin):
    list_display = [
        'is_active',
        'name',
        'score',
    ]


class EvaluationAdmin(admin.ModelAdmin):
    list_display = [
        'evaluator',
        'evaluatee',
        'get_parameters',
        'expiry_days',
        'comment',
        'is_active',
        'is_evaluated',
        'is_expired',
        'is_completed',
        'is_expirable'
    ]

    def get_parameters(self, obj):
        parameters = obj.parameters.all()
        return ', '.join([parameter.name for parameter in parameters])

    get_parameters.short_description = 'Parameters'


class IsEvaluatedEvaluatorFilter(admin.SimpleListFilter):
    title = 'Evaluator'
    parameter_name = 'is_evaluated_evaluator'

    def lookups(self, request, model_admin):

        evaluators = Evaluation.objects.filter(evaluator__isnull=False).values_list('evaluator', 'evaluator__username').distinct()
        evaluator_choices = [(evaluator_id, username) for evaluator_id, username in evaluators]
        return evaluator_choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(evaluation__is_evaluated=True, evaluation__evaluator=self.value())

class IsEvaluatedEvaluateeFilter(admin.SimpleListFilter):
    title = 'Evaluatee'
    parameter_name = 'is_evaluated_evaluatee'

    def lookups(self, request, model_admin):

        evaluatees = Evaluation.objects.filter(evaluatee__isnull=False).values_list('evaluatee', 'evaluatee__username').distinct()
        evaluatee_choices = [(evaluatee_id, username) for evaluatee_id, username in evaluatees]
        return evaluatee_choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(evaluation__is_evaluated=True, evaluation__evaluatee=self.value())

class EvaluationScoreAdmin(admin.ModelAdmin):
    list_display = [
        'evaluation',
        'parameter',
        'parameter_rating',
        'is_active',
        'is_evaluated',
        'average_rating_for_evaluatee'
    ]

    list_filter = (
        IsEvaluatedEvaluatorFilter,
        IsEvaluatedEvaluateeFilter
    )

    def average_rating_for_evaluatee(self, obj):

        avg_rating = EvaluationScore.objects.filter(
            evaluation__evaluatee=obj.evaluation.evaluatee
        ).aggregate(Avg('parameter_rating__score'))
        return avg_rating['parameter_rating__score__avg'] or 0

    average_rating_for_evaluatee.short_description = 'Average Rating for Evaluatee'


admin.site.register(BaseEvaluation, BaseEvaluationAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(ParameterRating, ParameterRatingAdmin)
admin.site.register(EvaluationScore, EvaluationScoreAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
