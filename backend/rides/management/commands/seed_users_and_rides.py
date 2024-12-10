import random
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from users.models import User 
from rides.models import Ride, RideEvent  


class Command(BaseCommand):
    help = "Seed the database with Ride and RideEvent data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")
        self.seed_users()
        self.seed_rides()
        self.stdout.write("Seeding complete!")

    def seed_users(self):
        # Check if users exist, to avoid duplicates
        if User.objects.count() >= 10:
            self.stdout.write("Users already seeded.")
            return

        for i in range(10):  # Create 10 users
            User.objects.create_user(
                username=f"user_{i}",
                email=f"user_{i}@example.com",
                password="password123",
            )
        self.stdout.write("Users seeded.")

    def seed_rides(self):
        users = User.objects.all()
        if users.count() < 2:
            self.stdout.write("Not enough users to seed rides.")
            return

        riders = users[:5]  # First 5 users as riders
        drivers = users[5:]  # Last 5 users as drivers

        for i in range(10):  # Create 10 rides
            ride = Ride.objects.create(
                id_rider=random.choice(riders),
                id_driver=random.choice(drivers),
                status=random.choice(["en-route", "pickup", "dropoff"]),
                pickup_latitude=random.uniform(-90, 90),
                pickup_longitude=random.uniform(-180, 180),
                dropoff_latitude=random.uniform(-90, 90),
                dropoff_longitude=random.uniform(-180, 180),
                pickup_time=now(),
            )
            self.seed_ride_events(ride)

        self.stdout.write("Rides seeded.")

    def seed_ride_events(self, ride):
        for i in range(random.randint(1, 5)):  # Create 1-5 events per ride
            RideEvent.objects.create(
                id_ride=ride,
                description=f"Event {i+1} for Ride {ride.id_ride}",
            )
        self.stdout.write(f"Events seeded for Ride {ride.id_ride}.")
