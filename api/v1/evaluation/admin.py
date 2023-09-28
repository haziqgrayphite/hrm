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

    def parameters_display(self, obj):
        return linebreaksbr(self.get_parameters(obj))

    def get_evaluators(self, obj):
        evaluators = obj.evaluators.all()
        # return ', '.join([evaluator.username for evaluator in evaluators])
        return [evaluator.username for evaluator in evaluators]

    get_evaluators.short_description = 'Evaluators'

    def get_evaluatees(self, obj):
        evaluatees = obj.evaluatees.all()
        # return ', '.join([evaluatee.username for evaluatee in evaluatees])
        return [evaluatee.username for evaluatee in evaluatees]

    get_evaluatees.short_description = 'Evaluatees'

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
        'score',
    ]


class EvaluationAdmin(admin.ModelAdmin):
    list_display = [
        'evaluator',
        'evaluatee',
        'get_parameters',
        'is_active',
        'is_evaluated',
    ]

    def get_parameters(self, obj):
        parameters = obj.parameters.all()
        return ', '.join([parameter.name for parameter in parameters])

    get_parameters.short_description = 'Parameters'


class EvaluationScoreAdmin(admin.ModelAdmin):
    list_display = [
        'evaluation',
        'parameter',
        'parameter_rating',
        'is_active',
        'is_evaluated'
    ]


admin.site.register(BaseEvaluation, BaseEvaluationAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(ParameterRating, ParameterRatingAdmin)
admin.site.register(EvaluationScore, EvaluationScoreAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
