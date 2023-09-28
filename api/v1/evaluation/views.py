from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q
from .models import Evaluation, Parameter, ParameterRating, EvaluationScore
from .serializers import (
    ParameterSerializer,
    ParameterRatingSerializer,
    EvaluationSerializer,
    EvaluationScoreUpdateSerializer,
)


class GeneralAPIView(APIView):
    def get(self, request):
        parameters = Parameter.objects.filter(is_active=True)
        parameter_ratings = ParameterRating.objects.filter(is_active=True)

        parameter_data = ParameterSerializer(parameters, many=True).data
        parameter_rating_data = ParameterRatingSerializer(parameter_ratings, many=True).data

        response_data = {
            "parameter": parameter_data,
            "parameter_rating": parameter_rating_data,
        }

        return Response(response_data)


class EvaluationAPIView(APIView):

    def get(self, request):

        evaluator_id = request.data.get('evaluator_id')
        evaluatee_id = request.data.get('evaluatee_id')
        user = request.user

        if evaluator_id:

            evaluations = Evaluation.objects.filter(
                Q(evaluator=evaluator_id) & Q(is_evaluated=False)
            )
            serializer = EvaluationSerializer(evaluations, many=True)

        elif evaluatee_id:

            evaluations = Evaluation.objects.filter(
                Q(evaluatee=evaluatee_id) & Q(is_evaluated=False)
            )
            serializer = EvaluationSerializer(evaluations, many=True)

        elif user:

            evaluations = Evaluation.objects.filter(evaluator=user) | Evaluation.objects.filter(evaluatee=user)
            evaluations = evaluations.filter(is_evaluated=False)
            serializer = EvaluationSerializer(evaluations, many=True, context={'request': request})

        else:
            evaluations = Evaluation.objects.filter(is_evaluated=False)
            serializer = EvaluationSerializer(evaluations, many=True)

        return Response(serializer.data)


class UpdateEvaluationScores(APIView):
    def put(self, request):

        try:

            evaluation_scores_data = request.data.get('evaluation_scores', [])
            evaluation_id = request.data.get('evaluation_id')
            evaluation = Evaluation.objects.get(id=evaluation_id)

            for data in evaluation_scores_data:

                parameter_id = data['parameter']
                parameter_rating = data['parameter_rating']

                try:

                    evaluation_score = EvaluationScore.objects.get(evaluation=evaluation, parameter_id=parameter_id)
                    serializer = EvaluationScoreUpdateSerializer(evaluation_score, data=data, partial=True)

                    if serializer.is_valid():

                        serializer.save()
                        evaluation_score.is_evaluated = True
                        evaluation_score.save()

                    else:

                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                except EvaluationScore.DoesNotExist:

                    return Response(f"Parameter with ID {parameter_id} not found for this evaluation.",
                                    status=status.HTTP_404_NOT_FOUND)

            if all(evaluation_score.is_evaluated for evaluation_score in evaluation.evaluation_score.all()):
                evaluation.is_evaluated = True
                evaluation.save()

            msg = "Parameter ratings and is_evaluated flag updated successfully."

            return Response({'message': msg}, status=status.HTTP_201_CREATED)

        except Evaluation.DoesNotExist:

            msg = "Evaluation not found"
            return Response({'message': msg}, status=status.HTTP_404_NOT_FOUND)
