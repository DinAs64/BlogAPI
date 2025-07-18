from django.test import TestCase
from blog.serializers import PostSerializer, CommentSerializer
from blog.models import Post, Comment
from users.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class PostSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass1234", email="tester@example.com")
        self.post = Post.objects.create(
            title = "Test Post",
            content = "Test content for the post",
            author = self.user
        )

    def test_post_serializer_valid(self):
        serializer = PostSerializer(instance=self.post)
        data = serializer.data
        self.assertEqual(data['title'], "Test Post")
        self.assertEqual(data['content'], "Test content for the post")
        self.assertEqual(data['author'], self.user.id)

    def test_post_serializer_create(self):
        data = {
            'title' :"Another Post",
            "content": "More content",
            "author": self.user.id
        }
        serializer = PostSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        post = serializer.save()
        self.assertEqual(post.title, "Another Post")
        self.assertEqual(post.author, self.user)

class CommentSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='commenter', password='pass1234', email="commenter@example.com")
        self.post = Post.objects.create(
            title = "Commentable Post",
            content = "Post to get commented",
            author = self.user
        )
        self.comment = Comment.objects.create(
            post = self.post,
            content = "Comment text",
            author = self.user
        )

    def test_comment_serializer_valid(self):
        serializer = CommentSerializer(instance=self.comment)
        data = serializer.data
        self.assertEqual(data['post'], self.post.id)
        self.assertEqual(data['content'], "Comment text")
        self.assertEqual(data['author'], self.user.id)
    
    def test_comment_serializer_create(self):
        data = {
            'post': self.post.id,
            'author': self.user.id,
            'content': "Nice stuff"
        }
        serializer = CommentSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        comment = serializer.save()
        self.assertEqual(comment.content, "Nice stuff")
        self.assertEqual(comment.post, self.post)

    def test_comment_serializer_invalid(self):
        data = {
            "post": "",
            "author": self.user.id,
            "content": ""
        }
        serializer = CommentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('post', serializer.errors)
        self.assertIn('content', serializer.errors)