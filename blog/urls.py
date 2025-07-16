from django.urls import path, include
from .views import (
    PostListCreateView, PostRetriveUpdateDestroyView,
    CommentListCreateView, CommentRetriveUpdateDestroy
    )
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

urlpatterns = [
    path('blog_post/', PostListCreateView.as_view(), name="post-list"),
    path('blog_post/<int:pk>', PostRetriveUpdateDestroyView.as_view(), name="post-detail"),

    path('blog_post/<int:post_pk>/comments/', CommentListCreateView.as_view(), name="comment-list-create"),
    path('blog_post/<int:post_pk>/comments/<int:pk>/', CommentRetriveUpdateDestroy.as_view(), name="comment-detail"),
]