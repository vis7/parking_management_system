from datetime import time
from rest_framework.generics import ListCreateAPIView
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Booking, SlotSpace
from .serializers import BookingSerializer, SlotSpaceSerializer


class BookingView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ListAvailableSlot(APIView):
    def post(self, request):
        """
        This will take date, parking type and give available slots on that date
        """
        date = request.POST['date']
        slot_space = request.POST['slot_space']
        # vehicle_type = request.POST['vehicle_type']

        # specific parking slot's available parking time
        time_slots = []
        day_start_time = time(6,0,0)
        day_end_time = time(23,0,0)

        available_slots = Booking.objects.filter(book_date=date, slot_space=slot_space).values('start_time', 'end_time').order_by('start_time')

        if available_slots[0]['start_time'] != day_start_time:
            time_slots.append(day_start_time.strftime("%H:%M:%S") + " - " + available_slots[0]['start_time'].strftime("%H:%M:%S"))

        for i in range(len(available_slots) - 1):
            time_slots.append(available_slots[i]['end_time'].strftime("%H:%M:%S") + " - " + available_slots[i+1]['start_time'].strftime("%H:%M:%S"))

        if available_slots.last()['end_time'] != day_end_time:
            time_slots.append(available_slots.last()['end_time'].strftime("%H:%M:%S") + " - " + day_end_time.strftime("%H:%M:%S"))

        return Response(time_slots, status=status.HTTP_200_OK)


class ListFullDayParking(APIView):
    def post(self, request):
        """
        This will take date, parking type and give available slots on that date
        """
        date = request.POST['date']
        # slot_space = request.POST['slot_space']
        # vehicle_type = request.POST['vehicle_type']

        # list available parkings of specified vehicle_type and date
        # parking slot for with there is no booking in given date
        # bookings = Booking.objects.filter(book_date=date)
        # serializer = BookingSerializer(bookings, many=True)
        slot_spaces = SlotSpace.objects.exclude(booking__book_date=date)
        serializer = SlotSpaceSerializer(slot_spaces, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

