from django.shortcuts import render
from .models import Flight, Booking, Passenger, Item

# Homepage: list all flights
def home(request):
    flights = Flight.objects.all()  
    return render(request, 'home.html', {'flights': flights})

# Flight detail page: show flight info
def flight_detail(request, flight_id):
    flight = Flight.objects.get(id=flight_id) 
    return render(request, 'flight_detail.html', {'flight': flight})

# Booking page: create a booking for a flight
def book_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id) 
    if request.method == 'POST':
        pass
    return render(request, 'booking_form.html', {'flight': flight})
# Passenger page: create a passenger associated to the booking
def passenger_bookings(request, passenger_id):
    passenger = Passenger.objects.get(id=passenger_id)  
    bookings = Booking.objects.filter(passenger=passenger)
    return render(request, 'passenger_bookings.html', {'passenger': passenger, 'bookings': bookings})


