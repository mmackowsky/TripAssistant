# Generated by Django 4.2.3 on 2023-08-10 08:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="bio",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="name",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="nickname",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="surname",
        ),
        migrations.AddField(
            model_name="profile",
            name="image",
            field=models.ImageField(default="default.jpg", upload_to="profile_pics"),
        ),
        migrations.AddField(
            model_name="profile",
            name="user",
            field=models.OneToOneField(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
