# users/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import login
from django.db import transaction
from .models import CustomUser
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    UserProfileSerializer,
    TokenRefreshSerializer
)


class RegisterAPIView(APIView):
    """
    Register a new user and return user data without tokens
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            
            if serializer.is_valid():
                with transaction.atomic():
                    user = serializer.save()
                    
                    user_data = UserSerializer(user).data
                    return Response({
                        'message': 'User registered successfully. Please login to continue.',
                        'user': user_data
                    }, status=status.HTTP_201_CREATED)
            
            return Response({
                'error': 'Registration failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'error': 'Registration failed',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPIView(APIView):
    """
    Authenticate user and return user data with JWT tokens
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            
            if serializer.is_valid():
                user = serializer.validated_data['user']
                refresh_token = serializer.validated_data['refresh']
                access_token = serializer.validated_data['access']
                
                # Return user data with JWT tokens
                user_data = UserSerializer(user).data
                return Response({
                    'message': 'Login successful',
                    # 'user': user_data,
                    'tokens': {
                        'refresh': refresh_token,
                        'access': access_token,
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({
                'error': 'Login failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'error': 'Login failed',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LogoutAPIView(APIView):
    """
    Logout user by blacklisting their refresh token
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                    return Response({
                        'message': 'Logout successful'
                    }, status=status.HTTP_200_OK)
                except TokenError:
                    return Response({
                        'error': 'Invalid refresh token'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'error': 'Refresh token required'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': 'Logout failed',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TokenRefreshAPIView(APIView):
    """
    Refresh JWT access token using refresh token
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = TokenRefreshSerializer(data=request.data)
            
            if serializer.is_valid():
                return Response({
                    'access': serializer.validated_data['access']
                }, status=status.HTTP_200_OK)
            
            return Response({
                'error': 'Token refresh failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'error': 'Token refresh failed',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetailAPIView(APIView):
    """
    Get current user's profile information
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            serializer = UserSerializer(request.user)
            return Response({
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Failed to retrieve user data',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileUpdateAPIView(APIView):
    """
    Update current user's profile information
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            serializer = UserProfileSerializer(
                request.user, 
                data=request.data, 
                partial=True
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Profile updated successfully',
                    'user': UserSerializer(request.user).data
                }, status=status.HTTP_200_OK)
            
            return Response({
                'error': 'Profile update failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'error': 'Profile update failed',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserListAPIView(APIView):
    """
    Get list of all users (staff only)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Only staff users can view all users
        if not request.user.user_type == 'staff':
            return Response({
                'error': 'Permission denied. Staff access required.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            users = CustomUser.objects.all().order_by('-date_joined')
            serializer = UserSerializer(users, many=True)
            return Response({
                'users': serializer.data,
                'count': users.count()
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Failed to retrieve users',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)