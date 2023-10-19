from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from .serializers import LeaveRequestSerializer, LeaveRequestTLSerializer, LeaveRequestHRSerializer
from .models import LeaveRequestTL, LeaveRequestHR
from api.v1.leave.permission import IsTeamLeadOrReadOnly


class LeaveRequestView(APIView):

    def post(self, request, format=None):

        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveRequestTLUpdate(APIView):
    permission_classes = [IsTeamLeadOrReadOnly]

    def put(self, request, leave_request_tl_id):

        try:
            leave_request_tl = LeaveRequestTL.objects.get(id=leave_request_tl_id)
        except LeaveRequestTL.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LeaveRequestTLSerializer(leave_request_tl, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveRequestHRUpdate(APIView):

    def put(self, request, leave_request_hr_id):

        if request.user.role != "HR":
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            leave_request_hr = LeaveRequestHR.objects.get(id=leave_request_hr_id)
        except LeaveRequestHR.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LeaveRequestHRSerializer(leave_request_hr, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
