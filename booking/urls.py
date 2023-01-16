from django.urls import path
from .views import BookingView

app_name = "booking"

urlpatterns = [
    path("", BookingView.as_view(), name="booking"),
]
