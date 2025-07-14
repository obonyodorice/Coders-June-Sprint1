from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from users.models import CustomUser
from attendance.models import Attendance
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.contrib.auth import logout

@staff_member_required
def dashboard_home(request):
    today = timezone.now().date()
    context = {
        'total_users': CustomUser.objects.count(),
        'total_attendances': Attendance.objects.count(),
        'today_checkins': Attendance.objects.filter(date=today).count(),
        'active_users_today': Attendance.objects.filter(date=today).values('user').distinct().count(),
        'recent_checkins': Attendance.objects.select_related('user')
                                            .order_by('-date', '-check_in_time')[:10]
    }
    return render(request, 'dashboard/home.html', context)

@staff_member_required
def user_management(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    paginator = Paginator(users, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/users.html', {'page_obj': page_obj})

@staff_member_required
def attendance_records(request):
    records = Attendance.objects.select_related('user').order_by('-date', '-check_in_time')
    paginator = Paginator(records, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/records.html', {'page_obj': page_obj})

def logout_view(request):
    logout(request)
    return redirect('dashboard:home')
        