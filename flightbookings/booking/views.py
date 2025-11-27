from decimal import Decimal
from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages

from .models import Flight, Booking, Passenger, Item

# Homepage: list all flights
def home(request):
    flights = Flight.objects.all()
    return render(request, 'home.html', {'flights': flights})


BAGGAGE_COST = Decimal("237")
TERMINAL_FEE = Decimal("273")
INSURANCE_COST = Decimal("208")


def _get_active_passenger():
    passenger = Passenger.objects.first()
    if passenger:
        return passenger

    return Passenger.objects.create(
        name="Enzo Galang",
        gender="Male",
        birth_date=date(2000, 1, 1),
    )


def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    passenger = _get_active_passenger()
    existing_booking = (
        Booking.objects.filter(passenger=passenger, flight=flight)
        .order_by("-date")
        .first()
    )

    if request.method == "POST":
        baggage_qty = int(request.POST.get("baggage_qty", 0) or 0)
        include_terminal_fee = "terminal_fee" in request.POST
        include_insurance = "insurance" in request.POST
    else:
        baggage_qty = 0
        include_terminal_fee = True  # terminal fee is usually mandatory
        include_insurance = False

    add_on_breakdown = [{"label": "Flight Fare", "quantity": 1, "cost": flight.cost}]
    total_cost = flight.cost

    if baggage_qty > 0:
        baggage_cost = BAGGAGE_COST * baggage_qty
        add_on_breakdown.append(
            {
                "label": "Additional Baggage",
                "quantity": baggage_qty,
                "cost": baggage_cost,
            }
        )
        total_cost += baggage_cost

    if include_terminal_fee:
        add_on_breakdown.append(
            {"label": "Terminal Fee", "quantity": 1, "cost": TERMINAL_FEE}
        )
        total_cost += TERMINAL_FEE

    if include_insurance:
        add_on_breakdown.append(
            {"label": "Travel Insurance", "quantity": 1, "cost": INSURANCE_COST}
        )
        total_cost += INSURANCE_COST

    if request.method == "POST":
        booking = Booking.objects.create(
            passenger=passenger,
            flight=flight,
            total_cost=total_cost,
        )

        if baggage_qty > 0:
            baggage_total = BAGGAGE_COST * baggage_qty
            Item.objects.create(
                booking=booking,
                description="Additional Baggage",
                quantity=baggage_qty,
                cost=baggage_total,
            )

        if include_terminal_fee:
            Item.objects.create(
                booking=booking,
                description="Terminal Fee",
                quantity=1,
                cost=TERMINAL_FEE,
            )

        if include_insurance:
            Item.objects.create(
                booking=booking,
                description="Travel Insurance",
                quantity=1,
                cost=INSURANCE_COST,
            )

        messages.success(request, "Booking finalized successfully.")
        return redirect("passenger_bookings", passenger_id=passenger.id)

    context = {
        "flight": flight,
        "booking_date": timezone.now(),
        "baggage_qty": baggage_qty,
        "include_terminal_fee": include_terminal_fee,
        "include_insurance": include_insurance,
        "add_on_breakdown": add_on_breakdown,
        "total_cost": total_cost,
        "existing_booking": existing_booking,
        "baggage_cost": BAGGAGE_COST,
        "terminal_fee": TERMINAL_FEE,
        "insurance_cost": INSURANCE_COST,
    }

    return render(request, "booking_form.html", context)

def passenger_bookings(request, passenger_id):
    passenger = Passenger.objects.get(id=passenger_id)  
    bookings = Booking.objects.filter(passenger=passenger)
    
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            passenger.name = name
            
        dob = request.POST.get("dob")
        if dob:
            passenger.birth_date = dob
            
        gender = request.POST.get("gender")
        if gender:
            passenger.gender = gender
    
    return render(request, 'passenger_bookings.html', {'passenger': passenger, 'bookings': bookings})



