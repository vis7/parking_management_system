from datetime import date, timedelta
from rest_framework.test import APIClient, APITestCase, force_authenticate
from rest_framework import status
from django.urls import reverse

from .models import Booking
from accounts.models import User


class BookingTests(APITestCase):
    fixtures = ["accounts/fixtures/users.json"]

    def test_booking_24_hours_in_advance(self):
        """
        Make sure that user is not able to book before 24 hours
        """
        today = date.today().strftime("%Y-%m-%d")
        future_date = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")

        # user authentication
        user1 = User.objects.get(username="user1")
        self.client.force_authenticate(user=user1)

        url = reverse("booking:booking")
        data = {"book_date": today, "slot_space": 0}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {"book_date": future_date, "slot_space": 0}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_single_parking_space_on_given_date(self):
        """
        Make sure that user can book only signle slot for the day
        """
        future_date = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")

        # user authentication
        user1 = User.objects.get(username="user1")
        self.client.force_authenticate(user=user1)

        url = reverse("booking:booking")
        data = {"book_date": future_date, "slot_space": 0}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {"book_date": future_date, "slot_space": 1}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_parking_slot_not_occupied_by_others(self):
        """
        Make sure that user can only book slot which is not taken by other user
        """
        future_date = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")

        # user authentication
        user1 = User.objects.get(username="user1")
        self.client.force_authenticate(user=user1)

        url = reverse("booking:booking")
        data = {"book_date": future_date, "slot_space": 0}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # user authentication
        user2 = User.objects.get(username="user2")
        self.client.force_authenticate(user=user2)

        data = {"book_date": future_date, "slot_space": 0}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
