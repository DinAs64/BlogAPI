from rest_framework import serializers
from .models import Post, Comment
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content", "author", "created_at", "updated_at"]

    def validate_title(self, value):
        if value is None:
            raise serializers.ValidationError("Title is required")
        return value

    def validate_content(self, value):
        if value is None:
            raise serializers.ValidationError("Text is required")
        return value
    
   
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["post", "author", "content", "created_at"]
        read_only_fields = ['created_at', 'post', 'author']

    def validate_content(self, value):
        if value is None:
            raise serializers.ValidationError("Comment is required")
        return value