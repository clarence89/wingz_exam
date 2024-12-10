from django.db import models
from users.models import User


class Ride(models.Model):

    id_ride = models.AutoField(primary_key=True)

    RIDE_STATUS_CHOICES =  (
            ("en-route", "En-Route"),
            ("pickup", "Pickup"),
            ("dropoff", "Dropoff"),
        )
    status = models.CharField(
        choices=RIDE_STATUS_CHOICES, default="en-route", max_length=8
    )
    rider = models.ForeignKey(User, on_delete=models.CASCADE , related_name="rider")
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="driver")
    pickup_latitude = models.FloatField(null=True, blank=True)
    pickup_longitude = models.FloatField(null=True, blank=True)
    dropoff_latitude = models.FloatField(null=True, blank=True)
    dropoff_longitude = models.FloatField(null=True, blank=True)
    pickup_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.id_ride
    
class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name="ride_events")
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
