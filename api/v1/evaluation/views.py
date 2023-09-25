from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Evaluation
from .serializers import EvaluationSerializer


class EvaluationAPIView(APIView):

    def get(self, request, evaluator_id=None):

        evaluator_id = request.data.get('evaluator_id')
        evaluatee_id = request.data.get('evaluatee_id')

        if evaluator_id:

            evaluation = Evaluation.objects.filter(evaluator=evaluator_id)
            serializer = EvaluationSerializer(evaluation, many=True)

        elif evaluatee_id:

            evaluation = Evaluation.objects.filter(evaluatee=evaluatee_id)
            serializer = EvaluationSerializer(evaluation, many=True)

        else:
            evaluations = Evaluation.objects.all()
            serializer = EvaluationSerializer(evaluations, many=True)

        return Response(serializer.data)
