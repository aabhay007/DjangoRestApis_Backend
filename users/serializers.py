# users/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Item, FileUpload, CartItem, Cart, ContactMessage
import base64


# region user
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["name", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["name"],
        )

        user.is_superuser = False
        user.is_staff = False
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "is_superuser"]


# endregion


# region items
class ItemSerializer(serializers.ModelSerializer):
    image = serializers.CharField(write_only=True, required=False)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            "id",
            "name",
            "description",
            "price",
            "image",
            "image_url",
            "created_at",
            "updated_at",
        ]

    def get_image_url(self, obj):
        if obj.image:
            try:
                return f"data:image/png;base64,{base64.b64encode(obj.image).decode('utf-8')}"
            except Exception as e:
                print(f"Error encoding image: {e}")
                return None
        return None

    def create(self, validated_data):
        image_data = validated_data.pop("image", None)
        if image_data:
            try:
                format, img_str = image_data.split(";base64,")
                validated_data["image"] = base64.b64decode(img_str)
            except (ValueError, TypeError) as e:
                raise serializers.ValidationError(f"Invalid image format: {e}")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        image_data = validated_data.pop("image", None)
        if image_data:
            try:
                format, img_str = image_data.split(";base64,")
                validated_data["image"] = base64.b64decode(img_str)
            except (ValueError, TypeError) as e:
                raise serializers.ValidationError(f"Invalid image format: {e}")

        return super().update(instance, validated_data)


# endregion


#region cart
class CartItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name", read_only=True)
    item_price = serializers.DecimalField(source="item.price", max_digits=10, decimal_places=2, read_only=True)
    item_image_url = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "item", "item_name", "item_price", "item_image_url", "quantity", "added_at"]

    def get_item_image_url(self, obj):
        if obj.item.image:
            try:
                return f"data:image/png;base64,{base64.b64encode(obj.item.image).decode('utf-8')}"
            except Exception as e:
                print(f"Error encoding image: {e}")
                return None
        return None


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "created_at", "updated_at"]
        read_only_fields = ["user", "created_at", "updated_at"]


#endregion


#region file_upload
class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['file', 'email']
#endregion


#region contact_us
class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id','name', 'email', 'message']
#endregion