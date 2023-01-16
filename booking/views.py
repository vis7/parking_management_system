from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from .models import Booking
from .serializers import BookingSerializer
from rest_framework.response import Response
from rest_framework import status, permissions


class BookingView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
