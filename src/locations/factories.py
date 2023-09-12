from factory import Factory
from faker import Faker

from .models import Location

fake = Faker()


class LocationFactory(Factory):
    class Meta:
        model = Location

    location_name = fake.name()
    place_type = fake.text()
    city = fake.city()
    street = fake.address()
    postcode = fake.postcode()
