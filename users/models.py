from django.db import models
from django.contrib.auth.models import User
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
        return f'Profile of {self.user.username}'


# class Profile(models.Model):
#     name = models.CharField(max_length=50)
#     surname = models.CharField(max_length=50)
#     nickname = models.CharField(max_length=20)
#     bio = models.TextField(max_length=200)


class Images(models.Model):
    image = models.ImageField()
    uploaded_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateField()


class Reviews(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    place = models.CharField(max_length=100)
    date_posted = models.DateField()
    stars = models.PositiveIntegerField()
