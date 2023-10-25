from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    image = models.FileField(
        default="user_profile/default.jpg", upload_to="user_profile"
    )

    def __str__(self) -> str:
        return f"{self.user.username}"
