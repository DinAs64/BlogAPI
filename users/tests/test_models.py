from users.factories import UserFactory, UserProfileFactory
from django.test import TestCase

class UserFactoryTestcase(TestCase):
    def test_user_creation(self):
        user = UserFactory()
        self.assertTrue(user.username.startswith("user"))

    def test_user_profile_creation(self):
        user_profile = UserProfileFactory()
        self.assertEqual(user_profile.bio, "Default bio")
        self.assertEqual(user_profile.location, "Default Location")
        self.assertIsNone(user_profile.date_of_birth)