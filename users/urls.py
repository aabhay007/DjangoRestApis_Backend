# users/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LoginView, UserView, ItemListCreateView, ItemDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserView.as_view(), name='user'),
    path('items/', ItemListCreateView.as_view(), name='item-list'),
    path('add-item/', ItemListCreateView.as_view(), name='create-item'),
    path('item-detail/<int:pk>/', ItemDetailView.as_view(), name='item-detail'),
    path('update-item/<int:pk>/', ItemDetailView.as_view(), name='update-item'),
    path('delete-item/<int:pk>/', ItemDetailView.as_view(), name='delete-item'),
]
