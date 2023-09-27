from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Evaluation, Parameter, ParameterRating
from .serializers import ParameterSerializer, ParameterRatingSerializer, EvaluationSerializer


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

    def get(self, request, evaluator_id=None):

        user = request.user

        evaluations = Evaluation.objects.filter(evaluator=user) | Evaluation.objects.filter(evaluatee=user)
        evaluations = evaluations.filter(is_evaluated=False)
        serializer = EvaluationSerializer(evaluations, many=True, context={'request': request})

        return Response(serializer.data)


class EvaluationDetailView(APIView):
    def get(self, request, pk):

        try:
            evaluation = Evaluation.objects.get(pk=pk)

        except Evaluation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EvaluationSerializer(evaluation)

        return Response(serializer.data)


class UpdateEvaluationParameters(APIView):
    def put(self, request, evaluatee_id):

        try:

            evaluation = Evaluation.objects.get(evaluatee__id=evaluatee_id)

            parameter_data = request.data.get('parameters', [])

            for param_data in parameter_data:

                parameter_id = param_data.get('parameter_id')
                rating_id = param_data.get('rating_id')

                if parameter_id is None or rating_id is None:
                    return Response({"message": "Both parameter_id and rating_id must be provided"},
                                    status=status.HTTP_400_BAD_REQUEST)

        except Evaluation.DoesNotExist:
            return Response({"message": "Evaluation not found"}, status=status.HTTP_404_NOT_FOUND)

