from django.urls import path
from .views import BookingView, ListAvailableSlot, ListFullDayParking

app_name = "booking"

urlpatterns = [
    path("", BookingView.as_view(), name="booking"),
    path("list_available_slots/", ListAvailableSlot.as_view(), name="list_available_slots"),
    path("list_fullday_parking/", ListFullDayParking.as_view(), name="list_fullday_parking"),
]
