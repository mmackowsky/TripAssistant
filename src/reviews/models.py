from django.db import models
from django.utils import timezone

from users.models import Profile
from locations.models import Location


class Images(models.Model):
    image = models.ImageField()
    uploaded_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)


class Reviews(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    date_posted = models.DateTimeField(default=timezone.now)
    # stars = models.PositiveIntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)

    def get_location_name(self):
        return self.location.name
