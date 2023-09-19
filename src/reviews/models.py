from django.db import models
from django.utils import timezone

from locations.models import Location
from users.models import Profile


class Reviews(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, help_text="author of the review"
    )
    content = models.CharField(max_length=500)
    date_posted = models.DateTimeField(default=timezone.now)
    stars = models.PositiveIntegerField(default=0)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, default=None, related_name="reviews"
    )

    def get_location_name(self) -> str:
        return self.location.name
