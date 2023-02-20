from django.db import models
from accounts.models import User
from .constants import SLOT_SPACE


class Premise(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class VehicleType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class SlotSpace(models.Model):
    name = models.CharField(max_length=32)
    vehicle_type = models.ForeignKey(
        VehicleType, on_delete=models.CASCADE, related_name="slot_space"
    )
    premise = models.ForeignKey(
        Premise, on_delete=models.CASCADE, related_name="slot_space"
    )
    rate_per_hour = models.DecimalField(max_digits=3, decimal_places=0)

    def __str__(self):
        return self.name + " " + str(self.vehicle_type) + " " + str(self.premise)


class Booking(models.Model):
    book_date = models.DateField()
    slot_space = models.ForeignKey(
        SlotSpace, on_delete=models.CASCADE, related_name="booking"
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booking")

    # class Meta:
    #     unique_together = (("book_date", "user"),)

    def __str__(self):
        return (
            str(self.book_date) + " " + str(self.slot_space) + " " + self.user.username
        )
