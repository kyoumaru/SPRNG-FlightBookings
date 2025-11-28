from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("book/<int:flight_id>/", views.book_flight, name="book_flight"),
    path("book/summary/<int:booking_id>/", views.booking_summary, name="booking_summary"),
    path("passenger/<int:passenger_id>/", views.passenger_bookings, name="passenger_bookings"),
]