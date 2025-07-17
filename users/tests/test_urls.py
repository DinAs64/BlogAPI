from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import UserLoginViewSet

class TestUserURLs(SimpleTestCase):
    def test_user_list_url_is_resolvable(self):
        url = reverse('user_register-list')
        self.assertEqual(resolve(url).func.cls, UserLoginViewSet)

    def test_user_detail_url_resolves(self):
        url = reverse('user_register-detail', kwargs={"pk": 1})
        resolved = resolve(url)
        self.assertEqual(resolved.func.cls, UserLoginViewSet)

    def test_user_profile_list_url(self):
        url = reverse('user_profile-list', kwargs={'user_register_pk': 1})
        self.assertEqual(resolve(url).func.cls.__name__, 'UserProfileViewSet')