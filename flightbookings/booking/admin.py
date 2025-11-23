from django.contrib import admin
from .models import Passenger, Flight, Booking, Item

# Register models to appear in admin
@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gender', 'birth_date')
    search_fields = ('name', 'gender')

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('id', 'origin', 'destination', 'cost')
    search_fields = ('origin', 'destination')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'passenger', 'flight', 'date', 'total_cost')
    list_filter = ('date',)
    search_fields = ('passenger__name', 'flight__origin', 'flight__destination')

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'description', 'quantity', 'cost')
    search_fields = ('description', 'booking__passenger__name', 'booking__flight__origin')


# Register your models here.
