from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    TokenRefreshAPIView,
    UserDetailAPIView,
    UserProfileUpdateAPIView,
    UserListAPIView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshAPIView.as_view(), name='token_refresh'),
    path('profile/', UserDetailAPIView.as_view(), name='user_detail'),
    path('profile/update/', UserProfileUpdateAPIView.as_view(), name='profile_update'),
    path('list/', UserListAPIView.as_view(), name='user_list'),
]
