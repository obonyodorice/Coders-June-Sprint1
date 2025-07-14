from django.urls import path
from .views import *

urlpatterns = [
    path('check_in/', CheckInView.as_view(), name='check_in'),
    path('check_out/', CheckOutView.as_view(), name='check_out'),
]
