from rest_framework import serializers
from .models import Post, Comment
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content", "author", "create_at", "updated_at"]

    def 
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["post", "author", "content", "create_at"]
        