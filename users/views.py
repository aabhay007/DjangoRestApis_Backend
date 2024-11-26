# users/views.py

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, login
from .serializers import RegisterSerializer, UserSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404
from .serializers import ItemSerializer, FileUploadSerializer
from .models import Item, Cart, CartItem
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsSuperUserOrReadOnly
from django.core.mail import EmailMessage
from rest_framework import generics
from django.contrib.auth.models import User


# region Authentication
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Generate refresh token
            refresh = RefreshToken.for_user(user)
            refresh.payload["is_superuser"] = user.is_superuser
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response(
                {
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                status=200,
            )

        return Response({"error": "Invalid credentials"}, status=400)


# endregion


# region User
class UserView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


# Detail View for Retrieving, Updating, and Deleting a User
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def delete(self, request, *args, **kwargs):
        """
        Custom delete response.
        """
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


# List View for Listing and Creating Users
class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# endregion


# region Items
class ItemListCreateView(APIView):
    permission_classes = [IsSuperUserOrReadOnly]

    def get(self, request):
        search_query = request.query_params.get("search", None)
        if search_query:
            items = Item.objects.filter(name__icontains=search_query)
        else:
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
    permission_classes = [IsSuperUserOrReadOnly]

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


# endregion


#region Cart
class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        item_id = request.data.get("item_id")
        quantity = request.data.get("quantity", 1)

        if not item_id:
            return Response({"error": "Item ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        item = get_object_or_404(Item, id=item_id)

        # Get or create the cart for the current user
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Check if the item is already in the cart
        cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)

        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
#endregion

# region task
class FileUploadView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file_instance = serializer.save()
            uploaded_file = request.FILES["file"]
            content_type = uploaded_file.content_type
            email = EmailMessage(
                subject="File Uploaded",
                body="Please find the attached file.",
                to=[file_instance.email],
            )
            email.attach(
                file_instance.file.name, file_instance.file.read(), content_type
            )
            email.send()

            return Response(
                {"message": "File uploaded and email sent successfully."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# endregion
