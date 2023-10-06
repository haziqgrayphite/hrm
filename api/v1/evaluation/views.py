from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
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


class PendingEvaluationAPIView(APIView):

    def get(self, request):

        evaluator_id = request.data.get('evaluator_id')
        evaluatee_id = request.data.get('evaluatee_id')

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

        else:
            evaluations = Evaluation.objects.filter(is_evaluated=False)
            serializer = EvaluationSerializer(evaluations, many=True)

        return Response(serializer.data)


class CompletedEvaluationAPIView(APIView):

    def get(self, request):

        evaluator_id = request.data.get('evaluator_id')
        evaluatee_id = request.data.get('evaluatee_id')

        if evaluator_id:

            evaluations = Evaluation.objects.filter(
                Q(evaluator=evaluator_id) & Q(is_evaluated=True)
            )
            serializer = EvaluationSerializer(evaluations, many=True)

        elif evaluatee_id:

            evaluations = Evaluation.objects.filter(
                Q(evaluatee=evaluatee_id) & Q(is_evaluated=True)
            )
            serializer = EvaluationSerializer(evaluations, many=True)

        else:
            evaluations = Evaluation.objects.filter(is_evaluated=True)
            serializer = EvaluationSerializer(evaluations, many=True)

        return Response(serializer.data)


class UpdateEvaluationScores(APIView):
    def put(self, request):

        try:
            evaluation_scores_data = request.data.get('evaluation_scores', [])

            if evaluation_scores_data:
                first_data = evaluation_scores_data[0]
                evaluation_id = first_data.get('evaluation')
                evaluation_comment = first_data.get('evaluation_comment')
                evaluation = Evaluation.objects.get(id=evaluation_id)

                current_datetime = timezone.now()

                if evaluation.valid_until <= current_datetime:
                    evaluation.is_expired = True
                    msg = "Evaluation is expired and cannot be updated."

                    return Response({'message': msg}, status=status.HTTP_400_BAD_REQUEST)

            for data in evaluation_scores_data:
                parameter_id = data['parameter']
                comments = data.get('comments', '')

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
                    msg = f"Parameter with ID {parameter_id} not found for this evaluation."

                    return Response({'message': msg}, status=status.HTTP_404_NOT_FOUND)

                try:
                    parameter = Parameter.objects.get(id=parameter_id)
                    parameter.comments = comments
                    parameter.save()
                except Parameter.DoesNotExist:
                    msg = f"Parameter with ID {parameter_id} not found."

                    return Response({'message': msg}, status=status.HTTP_404_NOT_FOUND)

            if all(evaluation_score.is_evaluated for evaluation_score in evaluation.evaluation_score.all()):
                evaluation.is_evaluated = True
                evaluation.is_completed = True
                evaluation.comment = evaluation_comment
                evaluation.save()

            msg = "Parameter ratings and comments updated successfully."

            return Response({'message': msg}, status=status.HTTP_201_CREATED)

        except Evaluation.DoesNotExist:
            msg = "Evaluation not found"

            return Response({'message': msg}, status=status.HTTP_404_NOT_FOUND)
