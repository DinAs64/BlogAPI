import factory
from blog.models import Post, Comment
from users.factories import UserFactory
from django.utils import timezone
from factory import LazyFunction, Faker


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
    
    title = Faker('sentence')
    content = Faker('paragraph', nb_sentences=5)
    author = factory.SubFactory(UserFactory)
    created_at = LazyFunction(timezone.now)
    updated_at = LazyFunction(timezone.now)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(UserFactory)
    content = Faker('paragraph', nb_sentences=5)
    created_at = LazyFunction(timezone.now)


