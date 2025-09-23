from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from django.db.models import Q

from teams.models import PlayerProfile

User = get_user_model()

class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name  = serializers.CharField()
    email      = serializers.EmailField()
    phone      = serializers.CharField()
    username   = serializers.CharField()
    password   = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate_password(self, value):
        # Build a temp user for context (helps UserAttributeSimilarityValidator)
        temp_user = User(
            username=self.initial_data.get("username", ""),
            email=self.initial_data.get("email", ""),
            first_name=self.initial_data.get("first_name", ""),
            last_name=self.initial_data.get("last_name", ""),
        )
        try:
            validate_password(value, temp_user)  # runs all AUTH_PASSWORD_VALIDATORS
        except DjangoValidationError as e:
            # Convert Django’s ValidationError to DRF’s, preserving messages
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, data):
        # Optional: normalize for case-insensitive uniqueness checks
        email_ci = data["email"].lower()
        username_ci = data["username"].lower()

        if User.objects.filter(Q(email__iexact=email_ci) | Q(username__iexact=username_ci)).exists():
            raise serializers.ValidationError("Email or username already exists.")
        return data

    def create(self, validated_data):
        # Prefer create_user: sets password hash, may normalize username/email
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        # If your custom User doesn't normalize email/username, do it beforehand:
        # user.email = user.email.lower(); user.username = user.username.lower(); user.save(update_fields=["email","username"])
        return user

class ProfileSerializerModel(serializers.ModelSerializer):
    # Create function for getting user profile photo from storage
    class Meta:
        model = PlayerProfile
        fields = '__all__'
        
class UserSerializerModel(serializers.ModelSerializer):
    profile = ProfileSerializerModel

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'phone')
