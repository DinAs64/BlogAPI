from blog.factories import PostFactory, CommentFactory
from django.test import TestCase
from django.utils import timezone, dateformat

class BlogTestCase(TestCase):
    def test_post_creation(self):
        post = PostFactory()
        self.assertIsInstance(post.title, str)
        self.assertTrue(len(post.title) > 0)

        self.assertIsInstance(post.content, str)
        self.assertTrue(len(post.content) > 0)

        self.assertAlmostEqual(post.created_at.date(), timezone.now().date())
        self.assertAlmostEqual(post.updated_at.date(), timezone.now().date())


    def test_comment_creation(self):
        comment = CommentFactory()

        self.assertIsInstance(comment.content, str)
        self.assertTrue(len(comment.content) > 0)

        self.assertAlmostEqual(comment.created_at.date(), timezone.now().date())
