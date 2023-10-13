from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Q
from django.db.models import Max
from .models import Evaluation, Parameter, ParameterRating, OverallEvaluationScore
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

        evaluator_id = request.query_params.get('evaluator_id')
        evaluatee_id = request.query_params.get('evaluatee_id')

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
        evaluator_id = request.query_params.get('evaluator_id')
        evaluatee_id = request.query_params.get('evaluatee_id')

        if evaluator_id:
            evaluations = Evaluation.objects.filter(
                Q(evaluator=evaluator_id) & Q(is_evaluated=True)
            )
        elif evaluatee_id:
            evaluations = Evaluation.objects.filter(
                Q(evaluatee=evaluatee_id) & Q(is_evaluated=True)
            )
        else:
            evaluations = Evaluation.objects.filter(is_evaluated=True)

        serialized_evaluations = []

        for evaluation in evaluations:
            evaluation_scores = OverallEvaluationScore.objects.filter(evaluation=evaluation)
            max_scores = ParameterRating.objects.aggregate(Max('score'))
            avg_rating = 0.0

            for score in evaluation_scores:
                max_parameter_rating = max_scores.get('score__max', 0)
                avg_rating += (score.parameter_rating.score / max_parameter_rating)

            avg_rating = (avg_rating / len(evaluation_scores)) * 100
            avg_rating = round(avg_rating, 2)
            evaluation.avg_rating = avg_rating

            evaluation_data = EvaluationSerializer(evaluation).data
            evaluation_data['avg_rating'] = avg_rating
            serialized_evaluations.append(evaluation_data)

        return Response(serialized_evaluations)


class AverageEvaluationAPIView(APIView):
    def get(self, request):
        evaluator_id = request.query_params.get('evaluator_id')
        evaluatee_id = request.query_params.get('evaluatee_id')

        if evaluator_id:
            evaluations = Evaluation.objects.filter(
                Q(evaluator=evaluator_id) & Q(is_evaluated=True)
            )
        elif evaluatee_id:
            evaluations = Evaluation.objects.filter(
                Q(evaluatee=evaluatee_id) & Q(is_evaluated=True)
            )
        else:
            evaluations = Evaluation.objects.filter(is_evaluated=True)

        serialized_evaluations = []

        for evaluation in evaluations:
            evaluation_scores = OverallEvaluationScore.objects.filter(evaluation=evaluation)
            max_scores = ParameterRating.objects.aggregate(Max('score'))
            avg_rating = 0.0

            for score in evaluation_scores:
                max_parameter_rating = max_scores.get('score__max', 0)
                avg_rating += (score.parameter_rating.score / max_parameter_rating)

            avg_rating = (avg_rating / len(evaluation_scores)) * 100
            avg_rating = round(avg_rating, 2)

            evaluation.avg_rating = avg_rating
            evaluation_data = EvaluationSerializer(evaluation).data
            evaluation_data['avg_rating'] = avg_rating

            serialized_evaluations.append(evaluation_data)

        if evaluatee_id:
            overall_avg_rating = sum(evaluation['avg_rating'] for evaluation in serialized_evaluations) / len(
                serialized_evaluations)
            overall_avg_rating = round(overall_avg_rating, 2)
            return Response({'evaluations': serialized_evaluations, 'overall_avg_rating': overall_avg_rating})

        return Response(serialized_evaluations)


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
                    evaluation_score = OverallEvaluationScore.objects.get(
                        evaluation=evaluation,
                        parameter_id=parameter_id
                    )

                    serializer = EvaluationScoreUpdateSerializer(evaluation_score, data=data, partial=True)

                    if serializer.is_valid():
                        serializer.save()
                        evaluation_score.is_evaluated = True
                        evaluation_score.save()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                except OverallEvaluationScore.DoesNotExist:
                    msg = f"Parameter with ID {parameter_id} not found for this evaluation."

                    return Response({'message': msg}, status=status.HTTP_404_NOT_FOUND)

                try:
                    parameter = Parameter.objects.get(id=parameter_id)
                    parameter.comments = comments
                    parameter.save()
                except Parameter.DoesNotExist:
                    msg = f"Parameter with ID {parameter_id} not found."
                    return Response({'message': msg}, status=status.HTTP_404_NOT_FOUND)

            if all(evaluation_score.is_evaluated for evaluation_score in evaluation.overall_evaluation_scores.all()):
                evaluation.is_evaluated = True
                evaluation.is_completed = True
                evaluation.comment = evaluation_comment
                evaluation.save()

            msg = "Parameter ratings and comments updated successfully."
            return Response({'message': msg}, status=status.HTTP_201_CREATED)

        except Evaluation.DoesNotExist:
            msg = "Evaluation not found"
            return Response({'message': msg}, status=status.HTTP_404_NOT_FOUND)
