from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
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
# editable only by the owner 
# and 
#seen by all the users.####

#User profile, nested for each user id.
class UserProfileViewSet(ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwner]
    lookup_field = "id"

    def get_queryset(self):
        user_id = self.kwargs['user_register_pk']
        return UserProfile.objects.filter(user__id=user_id)