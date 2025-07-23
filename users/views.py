from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import User, UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from blog.permissions import IsAuthorOrAdmin, IsOwner
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.throttling import ScopedRateThrottle

#User login with permission and throttling.
class UserLoginViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login'

#User profile, nested for each user id.
class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwner]
    lookup_field = "id"

    def get_queryset(self):
        user_id = self.kwargs['user_register_pk']
        return UserProfile.objects.filter(user__id=user_id)
