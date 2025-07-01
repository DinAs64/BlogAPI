from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView, CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from .models import CustomUser, UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from blog.permissions import IsAuthorOrAdmin, IsUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

#USER_LOGIN.
class UserLoginView(ListAPIView, CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

#USER_PROFILE.
class UserProfileListCreateView(ListAPIView, CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsUser]

class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthorOrAdmin]