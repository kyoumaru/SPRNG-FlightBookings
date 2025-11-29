from django.db import models


class Flight(models.Model):
    flight_id = models.AutoField(db_column='Flight_ID', primary_key=True)
    origin = models.CharField(db_column='Origin', max_length=255)
    destination = models.CharField(db_column='Destination', max_length=255)
    departure = models.DateTimeField(db_column='Departure')
    arrival = models.DateTimeField(db_column='Arrival')
    flight_cost = models.DecimalField(db_column='Flight_Cost', max_digits=10, decimal_places=2)


    class Meta:
        managed = True
        db_table = 'flight'


    def __str__(self):
        return f"{self.origin} → {self.destination} ({self.departure.strftime('%Y-%m-%d %H:%M')})"




class Passenger(models.Model):
    passenger_id = models.AutoField(db_column='Passenger_ID', primary_key=True)
    first_name = models.CharField(db_column='First_Name', max_length=255)
    last_name = models.CharField(db_column='Last_Name', max_length=255)
    gender = models.CharField(db_column='Gender', max_length=255)
    birth_date = models.DateField(db_column='Birth_Date')


    class Meta:
        managed = True
        db_table = 'passenger'


    def __str__(self):
        return f"{self.first_name} {self.last_name}"




class Booking(models.Model):
    booking_id = models.AutoField(db_column='Booking_ID', primary_key=True)
    booking_date = models.DateField(db_column='Booking_Date', auto_now_add=True)
    total_cost = models.DecimalField(db_column='Total_Cost', max_digits=10, decimal_places=2)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, db_column='Passenger_ID')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, db_column='Flight_ID')


    class Meta:
        managed = True
        db_table = 'booking'


    def __str__(self):
        return f"{self.passenger} - {self.flight} (${self.total_cost})"




class AdditionalItems(models.Model):
    item_id = models.AutoField(db_column='Item_ID', primary_key=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, db_column='Booking_ID', related_name='items')
    item_description = models.CharField(db_column='Item_Description', max_length=255)
    addon_cost = models.DecimalField(db_column='Addon_Cost', max_digits=10, decimal_places=2)
    quantity = models.IntegerField(db_column='Quantity')


    class Meta:
        managed = True
        db_table = 'additional_items'


    def __str__(self):
        return f"{self.item_description} x{self.quantity} (${self.addon_cost})"