from django.db import models
from locations import models as locations_models


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    cuisine = models.CharField(max_length=50)
    location = models.ForeignKey(locations_models.Location, on_delete=models.CASCADE)


class Hotels(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(locations_models.Location, on_delete=models.CASCADE)


class Attractions(models.Model):
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=50)
    location = models.ForeignKey(locations_models.Location, on_delete=models.CASCADE)
