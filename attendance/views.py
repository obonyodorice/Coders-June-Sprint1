from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

from .models import Attendance
from .serializers import AttendanceSerializer


class CheckInView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        User checks in by providing role and department.
        """
        serializer = AttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        today = timezone.now().date()
        attendance, created = Attendance.objects.get_or_create(
            user=request.user,
            date=today,
            defaults={
                'role': serializer.validated_data['role'],
                'department': serializer.validated_data['department'],
                'status': 'checked_in'
            }
        )
        if not created:
            return Response(
                {'detail': 'Already checked in for today.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        attendance.check_in_time = timezone.now()
        attendance.save()
        return Response(
            AttendanceSerializer(attendance).data,
            status=status.HTTP_201_CREATED
        )


class CheckOutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        User checks out, optionally updating role and department.
        """
        today = timezone.now().date()
        try:
            attendance = Attendance.objects.get(user=request.user, date=today)
        except Attendance.DoesNotExist:
            return Response(
                {'detail': 'No check-in record found for today.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if attendance.status == 'checked_out':
            return Response(
                {'detail': 'Already checked out.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update optional fields
        role = request.data.get('role')
        department = request.data.get('department')
        if role:
            attendance.role = role
        if department:
            attendance.department = department

        attendance.check_out_time = timezone.now()
        attendance.status = 'checked_out'
        attendance.save()
        
        serialized = AttendanceSerializer(attendance)

        return Response({
            'message': 'Checked out successfully',
            'data': serialized.data
        }, status=status.HTTP_200_OK)


