import datetime
import pytz
from django.conf.global_settings import TIME_ZONE
from rest_framework import serializers
from rest_framework.serializers import ValidationError


from .models import Booking

tz = pytz.timezone(TIME_ZONE)


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["book_date", "slot_space"]

    def validate_book_date(self, book_date):
        """
        User can only book single parking space on any given date
        Booking should be made 24 hrs in advance
        """
        user = self.context["request"].user

        # User can only book single parking space on any given date
        booking = Booking.objects.filter(user=user, book_date=book_date).first()

        if booking:
            raise ValidationError(
                f"You booked slot space number: {booking.slot_space} for date: {booking.book_date}.\n User can only book single parking space on any given date."
            )

        # Booking should be made 24 hrs in advance
        slot_time = datetime.time(0)
        book_datetime = datetime.datetime.combine(book_date, slot_time)
        book_datetime = tz.localize(book_datetime)
        now_datetime = datetime.datetime.now()
        now_datetime = tz.localize(now_datetime)
        time_diff = book_datetime - now_datetime

        if (
            time_diff.total_seconds() <= 86400
        ):  # 60*60*24 = 86400 (secounds in 24 hours)
            raise ValidationError("Booking should be made 24 hrs in advance")
        return book_date

    def validate(self, data):
        """
        Space and slot is not occupied by others
        """
        book_date = data["book_date"]
        slot_space = data["slot_space"]

        # Slot space is not occupied by others on given date
        booking = Booking.objects.filter(book_date=book_date, slot_space=slot_space)
        if booking:
            raise ValidationError(
                "This slot is already taken, kindly book another slot."
            )
        return data
