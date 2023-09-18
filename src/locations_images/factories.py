import factory
from django.contrib.auth.models import User

from locations.models import Location
from users.models import Profile

from .models import Images


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    password = factory.Faker("password")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)


class LocationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Location

    # Tutaj dodaj odpowiednie pola i wartości, które chcesz użyć do utworzenia obiektu Location


class ImagesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Images

    image = factory.django.ImageField(filename="default_place_image.jpg")
    uploaded_by = factory.SubFactory(ProfileFactory)
    location = factory.SubFactory(LocationFactory)
