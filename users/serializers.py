from rest_framework import serializers
from .models import CustomUser, UserProfile
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

#CustmUser serialization.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'password_confirm', 'email']

#Field-level validation.
    #Username.
    def validate_username(self, value):
        # 1. Must be at least 6 characters.
        if len(value) < 6:
            raise serializers.ValidationError("Username must be at least 12 characters.")
        
        # 2. Check uniqueness.
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already in use.")

        # 3. Check alphanumeric.
        if not value.isalnum():
            raise serializers.ValidationError("Username must be alphanumeric.")
        
        # 4. Forbidden usernames.
        blocked = ['admin', 'root', 'superuser']
        if value.lower in blocked:
            raise serializers.ValidationError("This username is not allowed.")
        
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
        if CustomUser.objects.filter(email==mail).exists():
            raise serializers.ValidationError("Email already in  use.")
        # 2 Check format.
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Email is not valid.")
       

#Object-level validation.
    #Password.
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data


#UserProfile serialization.
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'bio', 'avatar', 'location', 'date_of_birth']