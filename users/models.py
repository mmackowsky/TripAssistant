from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    nickname = models.CharField(max_length=20)
    bio = models.TextField(max_length=200)


class Images(models.Model):
    image = models.ImageField()
    by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_posted = models.DateField()


class Reviews(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    place = models.CharField(max_length=100)
    date_posted = models.DateField()
    stars = models.PositiveIntegerField()
