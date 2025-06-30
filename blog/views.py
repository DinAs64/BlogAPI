from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AND
from .permissions import IsAuthorOrAdmin
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


#POST GenericsViews + Mixins.
# 1. Create and Read with user-login permission.
class PostListCreateView(
    GenericAPIView, CreateModelMixin,
    ListModelMixin
    ):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)

# 2. Update, Delete and Read-one with author or admin permission.   
class PostRetriveUpdateDestroyView(
    GenericAPIView, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin
    ):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrAdmin]

    def get(self, request):
        return self.retrive(request)
    def put(self, request):
        return self.update(request)
    def destroy(self, request):
        return self.destroy(request)

#COMMENT GenericViews + Mixins.
# 1. Create and Read with user-login permission.
class CommentListCreateView(
    GenericAPIView, ListModelMixin,
    CreateModelMixin
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)
    def post(self, request):
        return self.create(request)
    
# 2. Update, Delete and Read-one with author or admin permission.   
class CommentRetriveUpdateDestroy(
    GenericAPIView, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdmin]

    def get(self, request):
        return self.retrieve(request)
    def put(self, request):
        return self.update(request)
    def destroy(self, request):
        return self.destroy(request)
