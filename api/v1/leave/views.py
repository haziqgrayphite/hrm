from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LeaveRequestSerializer, LeaveRequestTLSerializer, LeaveRequestHRSerializer
from .models import LeaveRequestTL, LeaveRequestHR, LeaveRequest
from api.v1.accounts.models import RoleChoices
from api.v1.leave.permission import IsTeamLeadOrReadOnly


class LeaveRequestView(APIView):

    def get(self, request, leave_request_id=None, format=None):

        if leave_request_id is not None:
            try:
                leave_request = LeaveRequest.objects.get(id=leave_request_id)
                serializer = LeaveRequestSerializer(leave_request)
                return Response(serializer.data)
            except LeaveRequest.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            leave_requests = LeaveRequest.objects.all()
            serializer = LeaveRequestSerializer(leave_requests, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):

        serializer = LeaveRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, leave_request_id, format=None):

        try:
            leave_request = LeaveRequest.objects.get(id=leave_request_id)
        except LeaveRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LeaveRequestSerializer(leave_request, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, leave_request_id, format=None):

        try:
            leave_request = LeaveRequest.objects.get(id=leave_request_id)
        except LeaveRequest.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        leave_request.is_active = False
        leave_request.save()
        serializer = LeaveRequestSerializer(leave_request)

        return Response(serializer.data)


class LeaveRequestTLUpdate(APIView):
    permission_classes = [IsTeamLeadOrReadOnly]

    def put(self, request, leave_request_tl_id):

        try:
            leave_request_tl = LeaveRequestTL.objects.get(id=leave_request_tl_id)
        except LeaveRequestTL.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LeaveRequestTLSerializer(leave_request_tl, data=request.data, partial=True)
        if serializer.is_valid():
            leave_request = leave_request_tl.leave_request
            is_active = leave_request.is_active
            if not is_active:
                return Response({'detail': 'Leave request is not active'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveRequestHRUpdate(APIView):

    def put(self, request, leave_request_hr_id):

        user_role = request.user.role

        if user_role != RoleChoices.HR.value:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            leave_request_hr = LeaveRequestHR.objects.get(id=leave_request_hr_id)
        except LeaveRequestHR.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = LeaveRequestHRSerializer(leave_request_hr, data=request.data, partial=True)
        if serializer.is_valid():

            leave_request = leave_request_hr.leave_request
            is_active = leave_request.is_active
            if not is_active:
                return Response({'detail': 'Leave request is not active'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
