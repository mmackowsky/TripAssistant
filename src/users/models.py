from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    image = models.ImageField(default='user_profile/default.jpg', upload_to='user_profile')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return f'{self.user.username}'


# class Images(models.Model):
#     image = models.ImageField()
#     uploaded_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     date_posted = models.DateTimeField(default=timezone.now)
#     location = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)
#
#
# class Reviews(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     content = models.CharField(max_length=500)
#     date_posted = models.DateTimeField(default=timezone.now)
#     stars = models.PositiveIntegerField()
#     location = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)
