from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse

from blog.factories import PostFactory, CommentFactory
from users.factories import UserFactory, UserProfileFactory
from blog.models import Post, Comment

class PostViewTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_create_view(self):
        data = {
            "title": "New Post",
            "content": "Test content",
            "author": self.user.id 
        }
        response = self.client.post(reverse('post-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

    def test_post_update_view(self):
        post = PostFactory(author=self.user)
        url = reverse('post-detail', args=[post.id])

        response = self.client.put(url, {
            "title": "Updated",
            "content": post.content,
            "author": self.user.id
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated")

    def test_post_delete_view(self):
        post = PostFactory(author=self.user)
        url = reverse('post-detail', args=[post.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=post.id).exists())


class CommentViewTests(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.other_user = UserFactory()
        self.post = PostFactory(author=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_comments(self):
        CommentFactory.create_batch(3, post=self.post)
        url = reverse('comment-list', kwargs={'post_pk': self.post.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_comment(self):
        url = reverse('comment-list', kwargs={'post_pk': self.post.pk})
        data = {
            "post": self.post.id,
            "author": self.user.id,
            "content": "Nice blog post!"
            }

        response = self.client.post(url, data)
        print(response.status_code)
        print(response.data)  # Or response.content if raw

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().post, self.post)

    def test_retrieve_comment(self):
        comment = CommentFactory(post=self.post, content="Original")
        url = reverse('comment-detail', kwargs={
            'post_pk': self.post.pk,
            'pk': comment.pk
        })

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], "Original")

    def test_update_comment_by_author(self):
        comment = CommentFactory(post=self.post, content="Original", author=self.user)
        url = reverse('comment-detail', kwargs={'post_pk': self.post.pk, 'pk': comment.pk})

        response = self.client.put(url, {"content": "Updated"})
        print(response.status_code)
        print(response.data)  # Or response.content if raw

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], "Updated")

    def test_update_comment_by_non_author(self):
        comment = CommentFactory(post=self.post, author=self.other_user)
        url = reverse('comment-detail', kwargs={'post_pk': self.post.pk, 'pk': comment.pk})

        response = self.client.put(url, {"content": "Hacked update"})
        print(response.status_code)
        print(response.data)  # Or response.content if raw

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_by_author(self):
        comment = CommentFactory(post=self.post, author=self.user)
        url = reverse('comment-detail', kwargs={'post_pk': self.post.pk, 'pk': comment.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
