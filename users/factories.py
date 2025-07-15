import factory
from users.models import User, UserProfile

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.PostGenerationMethodCall('set_password', 'testpass')

class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile
    
    user = factory.SubFactory(UserFactory)
    bio = "Default bio"
    location = "Default Location"
    date_of_birth = None