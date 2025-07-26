from django.shortcuts import render
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AND
from .permissions import IsAuthorOrAdmin
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

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

    def list(self, request, *args, **kwargs):
        cache_key = f'post_list_{request.query_params.urlencode()}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)  # cache 5 minutes
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.clear()  # or just delete relevant keys if needed
        return response 

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
    
    def list(self, request, *args, **kwargs):
        post_pk = self.kwargs['post_pk']
        cache_key = f'comment_list_post_{post_pk}_{request.query_params.urlencode()}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            cache.set(cache_key, serializer.data, timeout=60 * 5)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 5)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        post_pk = self.kwargs['post_pk']
        post = Post.objects.get(pk=post_pk)
        serializer.save(author=self.request.user, post=post)

        keys_to_delete = [key for key in cache.keys(f'comment_list_post_{post_pk}_*')]
        for key in keys_to_delete:
            cache.delete(key)

# 2. Update, Delete and Read-one with author or admin permission.   
class CommentRetriveUpdateDestroy(RetrieveUpdateDestroyAPIView
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdmin]

    def get_queryset(self):
        post_pk = self.kwargs['post_pk']
        return Comment.objects.filter(post__pk=post_pk)
