# users/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    UserView,
    ItemListCreateView,
    ItemDetailView,
    FileUploadView,
    UserListView,
    UserDetailView,
    AddToCartView,
)

urlpatterns = [
    # region authhetication routes
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # endregion
    # region user routes
    path("user/", UserView.as_view(), name="user"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    # endregion
    # region item routes
    path("items/", ItemListCreateView.as_view(), name="item-list"),
    path("add-item/", ItemListCreateView.as_view(), name="create-item"),
    path("item-detail/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("update-item/<int:pk>/", ItemDetailView.as_view(), name="update-item"),
    path("delete-item/<int:pk>/", ItemDetailView.as_view(), name="delete-item"),
    # endregion
    # region cart
    path("cart/add/", AddToCartView.as_view(), name="add-to-cart"),
    # endregion
    # region task
    path("upload/", FileUploadView.as_view(), name="file-upload"),
    # endregion
]
