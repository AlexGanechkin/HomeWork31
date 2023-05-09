from factory.django import DjangoModelFactory
import factory

from ads.models import User, Category, Publication


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("name")
    slug = factory.Faker("ean", length=8)


class PublicationFactory(DjangoModelFactory):
    class Meta:
        model = Publication

    name = factory.Faker("name")
    price = 100
    category_id = factory.SubFactory(CategoryFactory)
    author_id = factory.SubFactory(UserFactory)
