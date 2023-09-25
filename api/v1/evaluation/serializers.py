from rest_framework import serializers
from .models import Evaluation


class EvaluationSerializer(serializers.ModelSerializer):
    evaluator_name = serializers.CharField(source='evaluator.username', read_only=True)
    evaluatee_name = serializers.CharField(source='evaluatee.username', read_only=True)
    parameters_names = serializers.SerializerMethodField()

    class Meta:
        model = Evaluation
        fields = [
            'id',
            'created_at',
            'updated_at',
            'evaluator',
            'evaluatee',
            'is_active',
            'is_evaluated',
            'evaluator_name',
            'evaluatee_name',
            'parameters_names',
        ]

    def get_parameters_names(self, obj):
        return [parameter.name for parameter in obj.parameters.all()]
