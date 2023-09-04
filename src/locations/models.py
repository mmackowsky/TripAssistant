from django.db import models


class Location(models.Model):
    place_type = models.CharField(max_length=50)
    location_name = models.CharField(max_length=85)
    street = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.location_name

    class Meta:
        ordering = ['location_name']
