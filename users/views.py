from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView, CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import authenticate
from rest_framework import status
from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from blog.permissions import IsAuthorOrAdmin, IsOwner
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

#User login with full crud.
class UserLoginViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

####TODO: make the user profile 
# editable by the owner 
# and 
#seen by all the users.####

#User profile, nested for each user id.
class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        user_id = self.kwargs['user_pk']
        return UserProfile.objects.filter(user__id=user_id)