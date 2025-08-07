from rest_framework import serializers
from django.db.models import Q
from .models import *

class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if User.objects.filter(Q(email=data["email"]) | Q(username=data["username"])).exists():
            raise serializers.ValidationError("Email or username already exists.")
        return data
    
    def create(self, validated_data):
        # Extract user-related fields
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        phone = validated_data.pop("phone")
        email = validated_data.pop("email")
        username = validated_data.pop("username")
        password = validated_data.pop("password")

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            phone=phone,
        )
        user.set_password(password)
        user.save()
        return user