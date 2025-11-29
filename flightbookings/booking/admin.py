from django.contrib import admin
from .models import Flight, Passenger, Booking, AdditionalItems


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_id', 'origin', 'destination', 'departure', 'arrival', 'flight_cost')
    list_filter = ('origin', 'destination')
    search_fields = ('origin', 'destination')


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('passenger_id', 'first_name', 'last_name', 'gender', 'birth_date')
    search_fields = ('first_name', 'last_name')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'passenger', 'flight', 'booking_date', 'total_cost')
    list_filter = ('booking_date',)


@admin.register(AdditionalItems)
class AdditionalItemsAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'booking', 'item_description', 'quantity', 'addon_cost')