from django.contrib import admin
from django.urls import path, include
from dashboard.views import logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('staff/', include('dashboard.urls'))
]
