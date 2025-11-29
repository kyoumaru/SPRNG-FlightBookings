from decimal import Decimal
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from .models import Flight, Booking, Passenger, AdditionalItems


# Homepage: list all flights
def home(request):
    flights = Flight.objects.all()
    return render(request, 'home.html', {'flights': flights})




def _get_active_passenger():
    passenger = Passenger.objects.last()
    # If last passenger does not exist, create a new placeholder
    if not passenger or passenger.first_name != "":
        passenger = Passenger.objects.create(
            first_name="",
            last_name="",
            birth_date=date(1111,1,1),
            gender=""
        )
    return passenger




def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, flight_id=flight_id)
    passenger = _get_active_passenger()


    existing_booking = (
        Booking.objects.filter(passenger=passenger, flight=flight)
        .order_by("-booking_date")
        .first()
    )


    BAGGAGE_COST = Decimal("237")
    TERMINAL_FEE = Decimal("273")
    INSURANCE_COST = Decimal("208")


    if request.method == "POST":
        baggage_qty = int(request.POST.get("baggage_qty", 0) or 0)
        include_terminal_fee = "terminal_fee" in request.POST
        include_insurance = "insurance" in request.POST
    else:
        baggage_qty = 0
        include_terminal_fee = True
        include_insurance = False


    add_on_breakdown = [{"label": "Flight Fare", "quantity": 1, "cost": flight.flight_cost}]
    total_cost = flight.flight_cost


    if baggage_qty > 0:
        baggage_cost = BAGGAGE_COST * baggage_qty
        add_on_breakdown.append(
            {"label": "Additional Baggage", "quantity": baggage_qty, "cost": baggage_cost}
        )
        total_cost += baggage_cost


    if include_terminal_fee:
        add_on_breakdown.append({"label": "Terminal Fee", "quantity": 1, "cost": TERMINAL_FEE})
        total_cost += TERMINAL_FEE


    if include_insurance:
        add_on_breakdown.append({"label": "Travel Insurance", "quantity": 1, "cost": INSURANCE_COST})
        total_cost += INSURANCE_COST


    if request.method == "POST":
        booking = Booking.objects.create(
            passenger=passenger,
            flight=flight,
            total_cost=total_cost,
        )


        if baggage_qty > 0:
            AdditionalItems.objects.create(
                booking=booking,
                item_description="Additional Baggage",
                quantity=baggage_qty,
                addon_cost=BAGGAGE_COST * baggage_qty,
            )


        if include_terminal_fee:
            AdditionalItems.objects.create(
                booking=booking,
                item_description="Terminal Fee",
                quantity=1,
                addon_cost=TERMINAL_FEE,
            )


        if include_insurance:
            AdditionalItems.objects.create(
                booking=booking,
                item_description="Travel Insurance",
                quantity=1,
                addon_cost=INSURANCE_COST,
            )


        messages.success(request, "Thanks for booking with Magis Air!")
        return redirect("passenger_bookings", passenger_id=passenger.passenger_id)


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
    passenger = get_object_or_404(Passenger, passenger_id=passenger_id)
    booking = Booking.objects.filter(passenger=passenger).last()


    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        if fname and lname:
            passenger.first_name = fname
            passenger.last_name = lname


        dob = request.POST.get("dob")
        if dob:
            passenger.birth_date = dob


        gender = request.POST.get("gender")
        if gender:
            passenger.gender = gender


        passenger.save()
        return redirect("booking_summary", booking_id=booking.booking_id)


    return render(request, 'passenger_bookings.html', {'passenger': passenger, 'booking': booking})




def booking_summary(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    addons = AdditionalItems.objects.filter(booking=booking)


    if request.method == "POST":
        # Finalize booking
        messages.success(request, "Thanks for booking with Magis Air!")
        return redirect("home")


    context = {
        "booking": booking,
        "flight": booking.flight,
        "passenger": booking.passenger,
        "addons": addons,
    }
    return render(request, "booking_summary.html", context)