from django.db import models
from django.urls import reverse


class Passenger(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=13)
    national_id = models.IntegerField()
    password_id = models.IntegerField()

    def __str__(self):
        return str(self.id)
    
    
    def get_absolute_url(self):
        return reverse('booking:passenger_detail', args=[self.id])


class TypeOfTrip(models.Model):
    type = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.id)


class FlightClass(models.Model):
    class_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.id)
    
    
    def get_absolute_url(self):
        return reverse('booking:flight_class_detail', args=[self.id])


class Aeroplane(models.Model):
    number_plate = models.CharField(max_length=100)
    capacity = models.IntegerField()

    @property
    def empty_sits(self):
        empty_sits = Sits.objects.filter(available=True, aeroplane=self).all()
        return len(empty_sits) # confirsm this syntax

    def __str__(self):
        return str(self.id)
    
    
    def get_absolute_url(self):
        return reverse('booking:aeroplane_detail', args=[self.id])
    
    


class Sits(models.Model):
    """Is there a better way(non redundant) to organize an aeroplane and its sits"""
    sit_no = models.CharField(max_length=6, unique=True)
    flight_class = models.ForeignKey(FlightClass,
                                 related_name="sits",
                                 on_delete=models.PROTECT)
    available = models.BooleanField(default=True)
    aeroplane = models.ForeignKey(Aeroplane, 
                                  related_name="sits",
                                  on_delete=models.PROTECT)
    
    class Meta:
        ordering = ['sit_no']
        indexes = [
            models.Index(fields=['sit_no'])
        ]

    
    
    def __str__(self):
        return str(self.id)
    
    
    def get_absolute_url(self):
        return reverse('booking:sit_detail', args=[self.id])
    


# class Time(models.Model):
#     dep_time = models.TimeField()
#     arrival_time = models.TimeField()
#     aeroplane_id = models.ForeignKey(Aeroplane,
#                                      related_name="aeroplane",
#                                      on_delete=models.PROTECT)
"""There is a many to many relationship between Schedule and flights.
A Schedule can have many flights and A Flight can have more than one
Schedule.
If a flight attendant want to view all schedules for particular origin to 
a particular destination and vice versa, you would need to implment this
many to many relationship
 I choose to implement this many to many relationship.
 It is not really necessary given that you must have: origin, dest, dep_date to search for a flight
""" 
class Schedule(models.Model):
    dep_date = models.DateField()
    arrival_date = models.DateField()
    dep_time = models.TimeField()
    arrival_time = models.TimeField()
    aeroplane = models.ForeignKey(Aeroplane,
                                     related_name="schedules",
                                     on_delete=models.PROTECT)
    # Am thinking of deviding this table into two separete relations(date, time)
    # time = models.ForeignKey(Time,
    #                          related_name="times",
    #                          on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)
    
    def get_absolute_url(self):
        return reverse('booking:schedule_detail', args=[self.id])


class Flight(models.Model):
    # Find a better name for this class: Price, FlightService?
    origin = models.CharField(max_length=100)
    dest = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    type_of_trip = models.ForeignKey(TypeOfTrip,
                                     related_name="flights",
                                     on_delete=models.PROTECT)
    schedules = models.ManyToManyField(Schedule)
   

    def __str__(self):
        return str(self.id)
    
    
    def get_absolute_url(self):
        return reverse('booking:flight_detail', args=[self.id])


class Booking(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Passenger, 
                                    related_name="bookings",
                                    on_delete=models.PROTECT)
    adults = models.IntegerField()
    youths = models.IntegerField()
    children = models.IntegerField()
    infants = models.IntegerField()
    
    
    
    flight = models.ForeignKey(Flight, 
                               related_name="bookings",
                               on_delete=models.PROTECT)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return str(self.id)
    
    def get_absolute_url(self):
        return reverse('booking:booking_detail', args=[self.id])
    
    
