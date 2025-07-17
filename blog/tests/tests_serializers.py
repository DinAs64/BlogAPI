from rest_framework.test import APISimpleTestCase
from blog.serializers import PostSerializer, CommentSerializer
from blog.models import Post, Comment
from django.contrib.auth import get_user_model