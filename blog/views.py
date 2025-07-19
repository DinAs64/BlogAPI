from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AND
from .permissions import IsAuthorOrAdmin
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

#POST views.
# 1. Create and Read with user-login permission.
class PostListCreateView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

# 2. Update, Delete and Read-one with author or admin permission.   
class PostRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrAdmin]

#COMMENT views.
# 1. Create and Read with user-login permission.
class CommentListCreateView(ListCreateAPIView
):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

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
