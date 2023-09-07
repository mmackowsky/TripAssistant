from django.db import models
from django.db.models import Avg


class Location(models.Model):
    place_type = models.CharField(max_length=50)
    location_name = models.CharField(max_length=85)
    street = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.location_name

    class Meta:
        ordering = ["location_name"]

    @property
    def avg_rating(self):
        avg_rating = self.reviews.aggregate(Avg("stars"))["stars__avg"]
        return round(avg_rating, 2) if avg_rating else "Not rated yet"
