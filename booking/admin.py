from django.contrib import admin
from .models import Booking, Premise, VehicleType, SlotSpace

# Register your models here.
admin.site.register(Booking)
admin.site.register(Premise)
admin.site.register(VehicleType)
admin.site.register(SlotSpace)
