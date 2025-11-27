from django.db import models

class Passenger(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    birth_date = models.DateField()

    def __str__(self):
        return self.name

class Flight(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Flight {self.id}: {self.origin} - {self.destination}"
    
class Booking(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.passenger.name} - {self.flight.origin} - {self.flight.destination}"

class Item(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.description} x{self.quantity} (${self.cost})"

# Create your models here.
