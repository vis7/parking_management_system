from django.db import models
from accounts.models import User
from .constants import SLOT_SPACE


class Booking(models.Model):
    book_date = models.DateField()
    slot_space = models.CharField(choices=SLOT_SPACE, max_length=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="booking")

    class Meta:
        unique_together = (("book_date", "user"),)

    def __str__(self):
        return (
            str(self.book_date) + " " + str(self.slot_space) + " " + self.user.username
        )
