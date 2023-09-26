from rest_framework import serializers
from .models import Evaluation, Parameter, ParameterRating
from api.v1.accounts.serializers import CustomUserSerializer


class ParameterRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterRating
        fields = ('id', 'name', 'score')


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('id', 'name', 'description', 'parameter_rating')


class EvaluationSerializer(serializers.ModelSerializer):
    evaluator = CustomUserSerializer()
    evaluatee = CustomUserSerializer()

    class Meta:
        model = Evaluation
        fields = (
            'id', 'evaluator', 'evaluatee', 'parameters', 'is_active', 'is_evaluated')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['evaluator'] = CustomUserSerializer(instance.evaluator).data
        representation['evaluatee'] = CustomUserSerializer(instance.evaluatee).data
        representation['parameters'] = [param.id for param in instance.parameters.all()]
        return representation
