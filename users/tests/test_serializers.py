from django.test import TestCase
from users.serializers import UserProfileSerializer, UserSerializer
from users.models import User, UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializersTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="mary", 
            email="mary@example.com", 
            password="Pass12345678!",
            )
    
    def test_user_serializer_output(self):
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(data['username'], "mary")
        self.assertEqual(data['email'], "mary@example.com")
        self.assertIn("id", data)

    def test_user_serializer_create(self):
        data = {
            "username": "georgio",
            "email": "georgio@example.com",
            "password": "Pass1234#",
            "password_confirm": "Pass1234#"
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.username, "georgio")


class UserProfileSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jacob", email="jacob@example.com", password="pass1234")
        self.profile = UserProfile.objects.create(
            user=self.user, 
            bio="Referee",
            location = "Valley",
            date_of_birth = None
            )

    def test_user_profile_serializer_output(self):
        serializer = UserProfileSerializer(instance=self.profile)
        data = serializer.data
        self.assertEqual(data['bio'], "Referee")
        self.assertEqual(data['location'], "Valley")
        self.assertIn('user', data)
        self.assertEqual(data['username'], "jacob")

    def test_user_profile_serializer_create(self):
        data = {
            "user" : self.user.id,
            "bio": "New bio",
        }
        serializer = UserProfileSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('user', serializer.errors)
        self.assertEqual(
        str(serializer.errors['user'][0]),
        "user profile with this user already exists."
        )
