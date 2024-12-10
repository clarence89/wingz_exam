# serializers.py
from rest_framework import serializers
from .models import Ride, RideEvent
from users.models import User

class UserRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)

class GetRideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = '__all__'

class RideSerializer(serializers.ModelSerializer):
    rider = UserRideSerializer(read_only=True)
    driver = UserRideSerializer(read_only=True)
    ride_events = GetRideEventSerializer(many=True, read_only=True)
    class Meta:
        model = Ride
        fields = '__all__'

class GetRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'

class RideEventSerializer(serializers.ModelSerializer):
    ride = GetRideSerializer(read_only=True)
    class Meta:
        model = RideEvent
        fields = '__all__'

