from django.urls import path, include
from .views import (
    PostListCreateView, PostRetriveUpdateDestroyView,
    CommentListCreateView, CommentRetriveUpdateDestroy
    )
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

urlpatterns = [
    path('blog_post/', PostListCreateView.as_view()),
    path('blog_post/<int:pk>', PostRetriveUpdateDestroyView.as_view()),

    path('blog_post/<int:post_pk>/comments/', CommentListCreateView.as_view()),
    path('blog_post/<int:post_pk>/comments/<int:pk>/', CommentRetriveUpdateDestroy.as_view()),
]