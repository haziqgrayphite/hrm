from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.accounts.models import RoleChoices
from api.v1.leave.permission import IsTeamLeadOrReadOnly
from .models import LeaveRequestTL, LeaveRequestHR, LeaveRequest, TeamLead, LeaveBalance
from .serializers import (LeaveRequestSerializer, LeaveRequestTLSerializer, LeaveRequestHRSerializer
, LeaveRequestTLLSerializer, LeaveRequestHRRSerializer, LeaveBalanceSerializer)

User = get_user_model()


class LeaveRequestView(APIView):

    def get(self, request, leave_request_id=None, format=None):

        if leave_request_id:

            try:
                leave_request = LeaveRequest.objects.filter(id=leave_request_id).first()
                serializer = LeaveRequestSerializer(leave_request)
                return Response(serializer.data)
            except LeaveRequest.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            leave_requests = LeaveRequest.objects.filter(user=request.user, is_active=True)
            serializer = LeaveRequestSerializer(leave_requests, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        user = request.user
        data = request.data

        leave_duration = data.get("leave_duration")

        if leave_duration == "Half-Day Leave":
            data.setdefault("leaves_required", 0.5)

        leave_balance = 0
        if 'sick_leave' in data and data['sick_leave'] == 1:
            leave_balance = self.get_leave_balance(user, 'Sick Leave')
        elif 'annual_leave' in data and data['annual_leave'] == 1:
            leave_balance = self.get_leave_balance(user, 'Annual Leave')
        elif 'casual_leave' in data and data['casual_leave'] == 1:
            leave_balance = self.get_leave_balance(user, 'Casual Leave')

        if leave_balance < data["leaves_required"]:
            msg = "You cannot generate the request. Insufficient leave balance."
            return Response({'message': msg}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = LeaveRequestSerializer(data=data)

            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_leave_balance(self, user, leave_type):
        # Retrieve the leave balance from the LeaveBalance model based on leave type
        try:
            leave_balance = LeaveBalance.objects.get(employee=user)

            if leave_type == "Sick Leave":
                return leave_balance.sick_leave_balance
            elif leave_type == "Annual Leave":
                return leave_balance.annual_leave_balance
            elif leave_type == "Casual Leave":
                return leave_balance.casual_leave_balance
            else:
                return leave_balance.accumulative_balance
        except LeaveBalance.DoesNotExist:
            return 0

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
            leave_request_tl = LeaveRequestTL.objects.filter(id=leave_request_tl_id).first()
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


class LeaveRequestTLPending(APIView):

    def get(self, request):
        try:
            user = request.user
            team_lead = TeamLead.objects.filter(user=user).first()
        except ObjectDoesNotExist:
            return Response({"detail": "User is not a team lead."},
                            status=status.HTTP_404_NOT_FOUND)

        leave_requests_tl = (LeaveRequestTL.objects.filter(
            leave_request__user__team__team_lead=team_lead,
            is_team_lead_approval=False
        ))
        serializer = LeaveRequestTLLSerializer(leave_requests_tl, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LeaveRequestTLApproved(APIView):

    def get(self, request):
        try:
            user = request.user
            team_lead = TeamLead.objects.filter(user=user).first()
        except ObjectDoesNotExist:
            return Response({"detail": "User is not a team lead."},
                            status=status.HTTP_404_NOT_FOUND)

        leave_requests_tl = (LeaveRequestTL.objects.filter(
            leave_request__user__team__team_lead=team_lead,
            is_team_lead_approval=True
        ))
        serializer = LeaveRequestTLLSerializer(leave_requests_tl, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LeaveRequestHrPending(APIView):

    def get(self, request):
        try:
            user = request.user
            if user.role == 'HR':

                leave_requests_hr = LeaveRequestHR.objects.filter( is_hr_approval=False)
                serializer = LeaveRequestHRRSerializer(leave_requests_hr, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"detail": "User is not a HR."},
                            status=status.HTTP_404_NOT_FOUND)


class LeaveRequestHrApproved(APIView):

    def get(self, request):
        try:
            user = request.user
            if user.role == 'HR':

                leave_requests_hr = LeaveRequestHR.objects.filter( is_hr_approval=True)
                serializer = LeaveRequestHRRSerializer(leave_requests_hr, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"detail": "User is not a HR."},
                            status=status.HTTP_404_NOT_FOUND)


class LeaveBalanceAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        users = User.objects.all()

        for user in users:
            leave_balance_data = {
                'employee': user.id,
                'sick_leave': 1,
                'annual_leave': 1,
                'casual_leave': 1,
            }

            leave_balance_serializer = LeaveBalanceSerializer(data=leave_balance_data)
            if leave_balance_serializer.is_valid():
                leave_balance_serializer.save()
            else:
                return Response(leave_balance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Leave balances created successfully'}, status=status.HTTP_201_CREATED)

