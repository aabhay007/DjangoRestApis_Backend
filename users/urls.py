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
    CartView,
    UpdateCartItemView,CreatePaymentIntentView, 
    stripe_webhook
)
from . import views

urlpatterns = [
    # region authhetication_routes
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # endregion
    # region user_routes
    path("user/", UserView.as_view(), name="user"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    # endregion
    # region item_routes
    path("items/", ItemListCreateView.as_view(), name="item-list"),
    path("add-item/", ItemListCreateView.as_view(), name="create-item"),
    path("item-detail/<int:pk>/", ItemDetailView.as_view(), name="item-detail"),
    path("update-item/<int:pk>/", ItemDetailView.as_view(), name="update-item"),
    path("delete-item/<int:pk>/", ItemDetailView.as_view(), name="delete-item"),
    # endregion
    # region cart_routes
    path("cart/add/", AddToCartView.as_view(), name="add-to-cart"),
    path('cart/', CartView.as_view(), name='view-cart'),
    path('cart/item/<int:cart_item_id>/', UpdateCartItemView.as_view(), name='update-cart-item'),
    # endregion
    # region payment_routes
     path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
    #endregion
    # region file_upload_routes
    path("upload/", FileUploadView.as_view(), name="file-upload"),
    # endregion
    # region contact_us_routes
    path('contact/', views.contact_us, name='contact-us'),
    #endregion
]
