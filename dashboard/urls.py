from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('users/', views.user_management, name='users'),
    path('records/', views.attendance_records, name='records'),
    path('logout_staff/', views.logout_view, name='logout_staff'),
]