from rest_framework import serializers
from .models import Evaluation, Parameter, ParameterRating, EvaluationScore
from api.v1.accounts.serializers import CustomUserSerializer


class ParameterRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterRating
        fields = ('id', 'name', 'score')


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'name', 'description', 'comments')


class EvaluationScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationScore
        fields = (
            'evaluation',
            'parameter',
            'parameter_rating',
            'is_active',
            'is_evaluated',
        )


class EvaluationSerializer(serializers.ModelSerializer):
    evaluator = CustomUserSerializer()
    evaluatee = CustomUserSerializer()
    evaluation_scores = EvaluationScoreSerializer(many=True, read_only=True, source='evaluation_score')

    class Meta:
        model = Evaluation
        fields = (
            'id',
            'evaluator',
            'evaluatee',
            'parameters',
            'expiry_days',
            'comment',
            'is_active',
            'is_evaluated',
            'is_expired',
            'is_completed',
            'is_expirable',
            'evaluation_scores'
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['evaluator'] = CustomUserSerializer(instance.evaluator).data
        representation['evaluatee'] = CustomUserSerializer(instance.evaluatee).data
        representation['parameters'] = [param.id for param in instance.parameters.all()]
        return representation


class EvaluationScoreUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationScore
        fields = ('parameter_rating',)
