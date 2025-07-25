from django.shortcuts import render
from rest_framework import filters
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AND
from .permissions import IsAuthorOrAdmin
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend

#POST views.
# 1. List with user-login permission and filters.
class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['author', 'created_at'] 
    search_fields = ['title', 'content'] 
    ordering_fields = ['created_at', 'title']

# 2. Update, Delete and Read-one with author or admin permission.   
class PostRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrAdmin]

#COMMENT views.
# 1. List with permission, throttling and filters.
class CommentListCreateView(ListCreateAPIView
):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'comment_create'

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['content']
    ordering_fields = ['created_at']

    def get_queryset(self):
        post_pk = self.kwargs['post_pk']
        return Comment.objects.filter(post_id=post_pk)
    
    def perform_create(self, serializer):
        post_pk = self.kwargs['post_pk']
        post = Post.objects.get(pk=post_pk)
        serializer.save(author=self.request.user, post=post)
# 2. Update, Delete and Read-one with author or admin permission.   
class CommentRetriveUpdateDestroy(RetrieveUpdateDestroyAPIView
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdmin]

    def get_queryset(self):
        post_pk = self.kwargs['post_pk']
        return Comment.objects.filter(post__pk=post_pk)
