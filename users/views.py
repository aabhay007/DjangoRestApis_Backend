# users/views.py

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from .serializers import RegisterSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from .serializers import ItemSerializer
from .models import Item
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from datetime import timedelta

class LogoutView(APIView):
     permission_classes = [IsAuthenticated]
def post(self, request):
        response = JsonResponse({'message': 'Logout successful'})
        # Clear the cookies by setting them to expire
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
  
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            
            # Generate access and refresh tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Set the cookies in the response
            response = JsonResponse({'message': 'Login successful'})
            response.set_cookie(
                'access_token', 
                access_token, 
                httponly=True,  # Secure HttpOnly cookie
                secure=True,  # Set to True if using HTTPS
                samesite='Strict',  # Ensures cookies are sent only in first-party context
                max_age=timedelta(hours=1)  # Optional: Set expiration time
            )
            response.set_cookie(
                'refresh_token', 
                str(refresh), 
                httponly=True, 
                secure=True,  # Set to True if using HTTPS
                samesite='Strict',
                max_age=timedelta(days=7)  # Optional: Set expiration time for refresh token
            )
            
            return response
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Check if we're in a development environment
            is_dev = request.get_host().startswith("localhost")

            # Set access and refresh tokens in HttpOnly cookies
            response = JsonResponse({'message': 'Login successful'})
            response.set_cookie(
                'access_token', access_token,
                httponly=True,
                secure=not is_dev,  # Use HTTPS only in production
                samesite='None' if not is_dev else 'Strict',  # 'None' for cross-origin requests
                max_age=timedelta(hours=1)  # Access token expires in 1 hour
            )
            response.set_cookie(
                'refresh_token', refresh_token,
                httponly=True,
                secure=not is_dev,  # Use HTTPS only in production
                samesite='None' if not is_dev else 'Strict',  # 'None' for cross-origin requests
                max_age=timedelta(days=7)  # Refresh token expires in 7 days
            )
            return response

        return JsonResponse({'error': 'Invalid credentials'}, status=400)

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("Cookies:", request.COOKIES)  # Debugging log for cookies
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class ItemListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    