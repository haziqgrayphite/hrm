from rest_framework.response import Response
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
