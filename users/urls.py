from django.urls import path, include
from .views import UserProfileViewSet, UserLoginViewSet
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

router = DefaultRouter()
router.register(r'users', UserLoginViewSet, basename='user')

profile_router = NestedDefaultRouter(router, r'users', lookup='user')
profile_router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(profile_router.urls)),
]