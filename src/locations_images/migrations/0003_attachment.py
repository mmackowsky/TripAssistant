# Generated by Django 4.2.3 on 2023-09-07 09:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("locations_images", "0002_alter_images_location"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="attachments")),
            ],
        ),
    ]