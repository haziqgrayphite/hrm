from django.contrib import admin
from django import forms
from .models import AssignedEvaluation, CustomUser, Parameter, ParameterRating, Evaluation, OverallEvaluationScore


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = AssignedEvaluation
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


class AssignedEvaluationAdmin(admin.ModelAdmin):
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

class OverallEvaluationScoreAdmin(admin.ModelAdmin):
    list_display = [
        'evaluation',
        'parameter',
        'parameter_rating',
        'is_active',
        'is_evaluated'
    ]

    list_filter = (
        IsEvaluatedEvaluatorFilter,
        IsEvaluatedEvaluateeFilter
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(AssignedEvaluation, AssignedEvaluationAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(ParameterRating, ParameterRatingAdmin)
admin.site.register(OverallEvaluationScore, OverallEvaluationScoreAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
