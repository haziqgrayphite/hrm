from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from zk import ZK
from .models import Attendance, Attendee
from django.contrib.auth import get_user_model
from .serializers import AttendanceSerializer, AttendeeSerializer

User = get_user_model()


class PostAttendanceAPIView(APIView):

    def post(self, request):

        try:

            zk = ZK('192.168.1.90', port=4370)

            conn = zk.connect()

            attendance = zk.get_attendance()

            user_info_list = zk.get_users()
            user_info_dict = {user.user_id: user.name for user in user_info_list}

            daily_attendance = {}

            for record in attendance:
                user_id = record.user_id
                user_name = user_info_dict.get(user_id, 'Unknown')
                timestamp = record.timestamp

                if timestamp.month == 10 and timestamp.year == 2023:
                    date = timestamp.date()

                    if timestamp.hour >= 8 and timestamp.hour < 24:
                        if date not in daily_attendance:
                            daily_attendance[date] = {}

                        if user_id not in daily_attendance[date]:
                            daily_attendance[date][user_id] = {
                                'user_name': user_name,
                                'check_in': timestamp,
                                'check_out': None
                            }
                        else:
                            daily_attendance[date][user_id]['check_out'] = timestamp

            for date, user_data in daily_attendance.items():
                for user_id, data in user_data.items():
                    user_name = data['user_name']
                    check_in = data['check_in']
                    check_out = data['check_out']

                    existing_record = Attendance.objects.filter(
                        attendance_user_id=user_id,
                        check_in__date=date
                    ).first()

                    if not existing_record:

                        new_record = Attendance(
                            attendance_user_id=user_id,
                            check_in=check_in,
                            check_out=check_out
                        )
                        new_record.save()
                    else:

                        existing_record.check_in = check_in
                        existing_record.check_out = check_out
                        existing_record.save()

            conn.disconnect()

            return Response({"message": "Attendance data has been posted and calculated successfully."},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExcelInsertAPIView(APIView):

    def post(self, request):

        excel_file_path = request.data.get('file_path')
        print(f"Received file path: {excel_file_path}")

        try:
            data = pd.read_excel(excel_file_path)
        except Exception as e:
            print(f"Error reading Excel file: {str(e)}")
            return (Response(
                {'error': 'Error reading Excel file', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            ))

        for index, row in data.iterrows():
            code = row['Code']
            employee_name = row['Employee Name']
            email = row['Emails']

            try:

                user = User.objects.get(username__iexact=employee_name, email__iexact=email)

            except User.DoesNotExist:
                return Response(
                    {'error': f'User with username {employee_name} and email {email} does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            attendee, created = Attendee.objects.get_or_create(user=user, email=email, attendance_user_id=code)
        return Response({'message': 'Data inserted successfully'}, status=status.HTTP_201_CREATED)


class PreviousDayAttendanceAPIView(APIView):
    def get(self, request):

        try:
            today = timezone.now()
            previous_day = today - timedelta(days=1)

            attendee_email = request.user.email
            attendee = Attendee.objects.get(email=attendee_email)

            attendance_entries = Attendance.objects.filter(
                attendance_user_id=attendee.attendance_user_id,
                check_in__date=previous_day
            )

            attendance_serializer = AttendanceSerializer(attendance_entries, many=True)
            attendee_serializer = AttendeeSerializer(attendee)

            return Response({
                'user_attendance': attendance_serializer.data,
                'attendee_details': attendee_serializer.data
            }, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'error': 'No attendee details found for the user.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
