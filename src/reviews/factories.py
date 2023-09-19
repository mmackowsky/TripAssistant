from django.contrib.auth.models import User
from factory import Factory
from factory import Faker as fk
from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from locations.models import Location

from .models import Reviews

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = fk("name")
    password = fk("password")


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = Location

    location_name = fake.company()


class ReviewsFactory(DjangoModelFactory):
    class Meta:
        model = Reviews

    user = SubFactory(UserFactory)
    location = SubFactory(LocationFactory)
    content = fake.text()
    stars = fake.random_int(1, 5)
