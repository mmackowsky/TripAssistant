# Generated by Django 4.2.3 on 2023-09-06 09:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("locations", "0006_delete_images"),
        ("locations_images", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="images",
            name="location",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="locations.location",
            ),
        ),
    ]
