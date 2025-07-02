from rest_framework import serializers
from .models import User, UserProfile
import re
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

#CustomUser serialization.
class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email']
        extra_kwargs = {
            'password' : {'write_only': True},
            'email' : {'required': True},
        }

#Field-level validation.
    #Username.
    def validate_username(self, value):
        # 1. Must be at least 6 characters.
        if len(value) < 5:
            raise serializers.ValidationError("Username must be at least 5 characters.")
        
        # 2. Check uniqueness.
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already in use.")

        # 3. Check alphanumeric.
        if not value.isalnum():
            raise serializers.ValidationError("Username must be alphanumeric.")
        
        # 4. Forbidden usernames.
        blocked = ['admin', 'root', 'superuser']
        if value.lower() in blocked:
            raise serializers.ValidationError("This username is not allowed.")
        
        return value
    
    #Password.
    def validate_password(self, value):
        # Check length and characters with regex.
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters.")
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError("Password must contain at least one number.")
        if not re.search(r"[!@#$%^&*()_+=\-{};:'\",.<>?/\\|]", value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value
    
    #Email.
    def validate_email(self, value):
        # 1 Normalize and Check uniqueness.
        mail = value.strip().lower()
        if User.objects.filter(email=mail).exists():
            raise serializers.ValidationError("Email already in  use.")
        # 2 Check format.
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Email is not valid.")
        return value
    
#Object-level validation.
    #Password.
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    #Override create(). Using 'create_us' to hash the pass and discard 'password_confirm'.
    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        return user

#UserProfile serialization.
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location', 'date_of_birth']