from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse

from users.factories import UserFactory, UserProfileFactory
from users.models import UserProfile
import users.managers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserLoginViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", email="tester@example.com", password="pass1234"    
        )
        self.other_user = User.objects.create_user(
            username="hacker", email="hacker@example.com", password="pass1234"
        )
        self.profile = UserProfile.objects.create(
            user=self.user, bio="testing_stuff", location="TheValley", date_of_birth=None
        )
        self.other_profile = UserProfile.objects.create(
            user=self.other_user, bio="hacking_stuff", location="Alcatraz", date_of_birth=None
        )
        self.url = reverse("user_profile-list", kwargs={"user_register_pk": self.user.pk})
        self.other_url = reverse("user_profile-list", kwargs={"user_register_pk": self.other_user.pk})

    def test_requires_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_view_own_profile(self):
        self.client.login(username="tester", password="pass1234")
        response = self.client.get(self.url)

        #print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK )
        self.assertEqual(response.data[0]["username"], self.user.username)

    def test_user_cannot_view_other_profile(self):
        self.client.login(username="tester", password="pass1234")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_user_can_update_own_profile(self):
        self.client.login(username="tester", password="pass1234")
        response = self.client.get(self.url, {"bio": "Updated bio"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, "Updated bio")

    def test_user_cannot_update_other_profile(self):
        self.client.login(username="tester", password="pass1234")
        response = self.client.get(self.other_url, {"bio": "Hacked"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

