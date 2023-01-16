import json
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User

# client = APIClient()


class AccountTests(APITestCase):
    fixtures = ["accounts/fixtures/users.json"]

    def test_registration_and_login(self):
        """
        user is able to register and using these credentials can login successfully
        """
        # registration
        url = reverse("accounts:registration")
        data = {
            "username": "user3",
            "email": "user3@gmail.com",
            "password": "Use@1234",
            "confirm_password": "Use@1234",
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            User.objects.get(username=data["username"]).username, data["username"]
        )

    def test_login(self):
        # loging
        url = reverse("accounts:login")
        data = {"username": "user1", "password": "Use@1234"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
