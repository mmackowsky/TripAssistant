from django.db import models


class Location(models.Model):
    place = models.CharField(max_length=50)
    city = models.CharField(max_length=85)
    street = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
