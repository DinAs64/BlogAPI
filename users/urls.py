from .views import UserProfileListCreateView, UserProfileDetailView, UserLoginView
from django.urls import path

urlpatterns = [
    path('login', UserLoginView.as_view()),
    path('profile/', UserProfileListCreateView.as_view()),
    path('profile/<int:pk>', UserProfileDetailView.as_view()),
]