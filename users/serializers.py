from rest_framework import serializers
from .models import CustomUser
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password_confirm', 'email']

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

    #TODO: add email validation and password confirmation
    def validate_email(self, value):
        pass
        

#Object-level validation.
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data