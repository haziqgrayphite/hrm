from datetime import timedelta, datetime
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from zk import ZK
from .models import Attendance, AttendanceStatus
from django.contrib.auth import get_user_model
from .serializers import AttendanceSerializer
from api.v1.accounts.serializers import CustomUserSerializer
from api.v1.leave.models import LeaveRequest

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

                date = timestamp.date()

                if timestamp.hour >= 8 and timestamp.hour < 24:
                    if date not in daily_attendance:
                        daily_attendance[date] = {}

                    if user_id not in daily_attendance[date]:
                        daily_attendance[date][user_id] = {
                            'user_name': user_name,
                            'check_in': timestamp,
                            'check_out': None,
                            'status': AttendanceStatus.PRESENT.value
                        }
                    else:
                        daily_attendance[date][user_id]['check_out'] = timestamp

            for date, user_data in daily_attendance.items():
                for user_id, data in user_data.items():
                    user_name = data['user_name']
                    check_in = data['check_in']
                    check_out = data['check_out']
                    status_value = data['status']
                    print(status_value)

                    existing_record = Attendance.objects.filter(
                        attendance_user_id=user_id,
                        check_in__date=date
                    ).first()

                    if not existing_record:
                        new_record = Attendance(
                            attendance_user_id=user_id,
                            check_in=check_in,
                            check_out=check_out,
                            status=status_value
                        )
                        new_record.save()
                    else:
                        existing_record.check_in = check_in
                        existing_record.check_out = check_out
                        existing_record.status = status_value
                        existing_record.save()

            conn.disconnect()

            return Response({"message": "Attendance data has been posted and calculated successfully."},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#
#
# # class ExcelInsertAPIView(APIView):
# #
# #     def post(self, request):
# #
# #         excel_file_path = request.data.get('file_path')
# #         print(f"Received file path: {excel_file_path}")
# #
# #         try:
# #             data = pd.read_excel(excel_file_path)
# #         except Exception as e:
# #             print(f"Error reading Excel file: {str(e)}")
# #             return (Response(
# #                 {'error': 'Error reading Excel file', 'details': str(e)},
# #                 status=status.HTTP_400_BAD_REQUEST
# #             ))
# #
# #         for index, row in data.iterrows():
# #             code = row['Code']
# #             employee_name = row['Employee Name']
# #             email = row['Emails']
# #
# #             try:
# #
# #                 user = User.objects.get(username__iexact=employee_name, email__iexact=email)
# #
# #             except User.DoesNotExist:
# #                 return Response(
# #                     {'error': f'User with username {employee_name} and email {email} does not exist'},
# #                     status=status.HTTP_404_NOT_FOUND
# #                 )
# #
# #             attendee, created = Attendee.objects.get_or_create(user=user, email=email, attendance_user_id=code)
# #         return Response({'message': 'Data inserted successfully'}, status=status.HTTP_201_CREATED)
#
#
class PreviousMonthAttendanceAPIView(APIView):
    def get(self, request):

        try:

            today = timezone.now()
            end_date = today - timedelta(days=1)
            start_date = end_date - timedelta(days=30)
            attendee_email = request.user.email
            user = User.objects.get(email=attendee_email)

            attendance_entries = Attendance.objects.filter(
                attendance_user_id=user.attendance_machine_code,
                check_in__date__range=[start_date, end_date],
            ).order_by('-check_out')

            all_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

            checkin_dates = [entry.check_in.date().strftime("%Y-%m-%d") for entry in attendance_entries]

            missing_dates = [date.strftime("%Y-%m-%d") for date in all_dates if
                             date.strftime("%Y-%m-%d") not in checkin_dates]

            missing_dates_filtered = [date for date in missing_dates if
                                      datetime.strptime(date, "%Y-%m-%d").weekday() not in [5, 6]]

            print(missing_dates_filtered)

            for missing_date in missing_dates_filtered:
                leave_request = LeaveRequest.objects.filter(
                    user=user,
                    start_date=missing_date,
                    end_date=missing_date
                ).first()
                # if leave_request:
            # The leave request for this missing date exists
            # You can process it as needed
            # print(missing_dates)

            for entry in attendance_entries:

                if entry.check_in and entry.check_out is None:
                    print(entry)
                    entry.status = AttendanceStatus.AMBIGUOUS.value
                    entry.save()

            attendance_serializer = AttendanceSerializer(attendance_entries, many=True)
            user_serializer = CustomUserSerializer(user)

            return Response({
                'user_attendance': attendance_serializer.data,
                'user_details': user_serializer.data
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'No user details found for the logged-in user.'},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SyncAttendanceAPIView(APIView):
    def post(self, request):

        try:

            attendance_entry = Attendance.objects.latest('created_at')
            print(attendance_entry)
            attendance_entry_date = attendance_entry.check_in
            print(attendance_entry_date)

            zk = ZK('192.168.1.90', port=4370)
            conn = zk.connect()
            attendance = zk.get_attendance()
            user_info_list = zk.get_users()
            user_info_dict = {user.user_id: user.name for user in user_info_list}

            machine_data_filtered = [entry for entry in attendance if entry.timestamp.replace(
                tzinfo=attendance_entry_date.tzinfo) > attendance_entry_date]

            print(machine_data_filtered)

            processed_entries = {}
            entry_count = {}
            for entry in machine_data_filtered:
                user_id = entry.user_id
                user_name = user_info_dict.get(user_id, 'Unknown')
                timestamp = entry.timestamp.replace(tzinfo=attendance_entry_date.tzinfo)
                print(timestamp)
                date = timestamp.date()

                if timestamp.hour >= 8 and timestamp.hour < 24:

                    if date not in processed_entries:
                        processed_entries[date] = {}
                        entry_count[date] = {}

                    if user_id not in processed_entries[date]:
                        processed_entries[date][user_id] = {
                            'user_name': user_name,
                            'check_in': timestamp,
                            'check_out': None
                        }
                        entry_count[date][user_id] = 1
                    else:
                        processed_entries[date][user_id]['check_out'] = timestamp
                        entry_count[date][user_id] += 1

            for date, user_data in processed_entries.items():
                for user_id, data in user_data.items():
                    user_name = data['user_name']
                    check_in = data['check_in']
                    check_out = data['check_out']
                    count = entry_count[date][user_id]
                    print(count)

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
                        if existing_record.check_in is None:
                            existing_record.check_in = check_in
                        if count == 1:
                            existing_record.check_out = check_in
                        else:
                            existing_record.check_out = check_out
                        existing_record.save()

            conn.disconnect()
            return Response({"message": "Attendance data has been posted and calculated successfully."},
                            status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
