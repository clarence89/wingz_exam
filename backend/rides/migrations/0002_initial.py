# Generated by Django 4.2.8 on 2024-12-10 03:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("rides", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="ride",
            name="id_driver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="driver",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="ride",
            name="id_rider",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rider",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]