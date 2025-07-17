from django.test import SimpleTestCase
from django.urls import reverse, resolve
import blog.views

class TestPostURLs(SimpleTestCase):
    def test_post_list_url_resolves(self):
        url = reverse('post-list')
        self.assertEqual(resolve(url).func.cls, blog.views.PostListCreateView)
    
    def test_post_detail_url_resolves(self):
        url = reverse('post-detail', kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.cls, blog.views.PostRetriveUpdateDestroyView)

    def test_comment_list_url_resolves(self):
        url = reverse('comment-list', kwargs={"post_pk": 1})
        self.assertEqual(resolve(url).func.cls, blog.views.CommentListCreateView)
    
    def test_comment_detail_url_resolves(self):
        url = reverse('comment-detail', kwargs={"post_pk": 1, "pk": 1})
        self.assertEqual(resolve(url).func.cls, blog.views.CommentRetriveUpdateDestroy)
