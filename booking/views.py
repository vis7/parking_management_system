from rest_framework.generics import ListCreateAPIView
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from .models import Booking
from .serializers import BookingSerializer


class BookingView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
