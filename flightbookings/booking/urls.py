from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("booki/<int:flight_id>/", views.book_flight, name="book_flight"),
    path("passenger/<int:passenger_id>/", views.passenger_bookings, name="passenger_bookings"),
]