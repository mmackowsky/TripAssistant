from django.db import models
from django.utils import timezone

from locations.models import Location
from users.models import Profile


class Images(models.Model):
    image = models.FileField(
        default="places/default_place_image.jpg", upload_to="places"
    )
    uploaded_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, default=None, related_name="images"
    )
