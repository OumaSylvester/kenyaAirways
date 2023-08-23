from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
# from .forms import validate_dep_date


class Passenger(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=13)
    national_id = models.IntegerField()
    passport_id = models.IntegerField()

    def __str__(self):
        return str(self.email)
    
    
    def get_absolute_url(self):
        return reverse('booking:passenger_detail', args=[self.id])


class TypeOfTrip(models.Model):
    type = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return str(self.type)


class SeatClass(models.Model):
    class_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.class_name)
    
    
    def get_absolute_url(self):
        return reverse('booking:flight_class_detail', args=[self.id])

class Route(models.Model):
    # Find a better name for this class: Price, FlightService?
    origin = models.CharField(max_length=100)
    dest = models.CharField(max_length=100)   
    
    price_A = models.DecimalField(max_digits=12, decimal_places=2)
    price_B = models.DecimalField(max_digits=12, decimal_places=2)
    price_C = models.DecimalField(max_digits=12, decimal_places=2)


    class Meta:
        verbose_name_plural = "Flights"
        indexes = [
            models.Index(fields=['origin'])
        ]
   

    def __str__(self):
        return str(self.origin + " - " + self.dest)
    
    
    def get_absolute_url(self):
        return reverse('booking:flight_detail', args=[self.id])
    
class Aeroplane(models.Model):
    number_plate = models.CharField(max_length=100, unique=True)
    capacity = models.IntegerField()
    route = models.ForeignKey(Route, 
                               related_name="aeroplanes",
                               on_delete=models.PROTECT)
   
    class Meta:
        verbose_name_plural = "Aeroplanes"

    def __str__(self):
        return str(self.number_plate)
    
    
    def get_absolute_url(self):
        return reverse('booking:aeroplane_detail', args=[self.id])
    

class Seat(models.Model):
    """Is there a better way(non redundant) to organize an aeroplane and its sits"""
    seat_no = models.CharField(max_length=6)
    seat_class = models.ForeignKey(SeatClass,
                                 related_name="seats",
                                 on_delete=models.PROTECT)
    available = models.BooleanField(default=True)
    aeroplane = models.ForeignKey(Aeroplane,
                                  related_name="seats",
                                  on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['seat_no']
        indexes = [
            models.Index(fields=['seat_no'])
        ]
        unique_together = ['seat_no', 'aeroplane']

    
    
    def __str__(self):
        return str(self.seat_no)
    
    
    def get_absolute_url(self):
        return reverse('booking:seat_detail', args=[self.id])
    

    
class Time(models.Model):
    dep_time = models.TimeField()
    arrival_time = models.TimeField() # validators=[MinValueValidator(dep_time, "Arrival time must not be depature time")])
    aeroplanes = models.ManyToManyField(Aeroplane,
                                     related_name="times",
                                     )

    def __str__(self):
        dep_str = self.dep_time.strftime("%H:%M:%S - ")
        arr_str = self.arrival_time.strftime("%H:%M:%S")
        return dep_str + arr_str
    
    class Meta:
        ordering = ['dep_time']
        indexes = [
            models.Index(fields=['dep_time', 'arrival_time'])
        ]

    def get_absolute_url(self):
        return reverse('booking:time_detail', args=[self.id])


class Schedule(models.Model):
    dep_date = models.DateField() # add validators
    arrival_date = models.DateField()# validators=[MinValueValidator(dep_date, "Arrivale date must not be before departure date")]) # must not be less than dep_date
    times = models.ManyToManyField(Time,
                                  related_name="schedules",
                                  )
    routes = models.ManyToManyField(Route,
                                       related_name="schedules")

    class Meta:
        verbose_name_plural = "Schedules"
        unique_together = ['dep_date', 'arrival_date']

    def __str__(self):
        date_str = self.dep_date.strftime("%Y/%m/%d - ") + (self.arrival_date.strftime("%Y/%m/%d"))
        return date_str
    
    def get_absolute_url(self):
        return reverse('booking:schedule_detail', args=[self.id])





class Booking(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Passenger, 
                                    related_name="bookings",
                                    on_delete=models.PROTECT)
    adults = models.IntegerField()
    youths = models.IntegerField()
    children = models.IntegerField()
    infants = models.IntegerField()
    
    
    
    route = models.ForeignKey(Route, 
                               related_name="bookings",
                               on_delete=models.PROTECT)
    schedule = models.ForeignKey(Schedule, 
                                 related_name="bookings",
                                 on_delete=models.PROTECT)
    time = models.ForeignKey(Time,
                             related_name="bookings",
                             on_delete=models.PROTECT)
    type_of_trip = models.ForeignKey(TypeOfTrip,
                                     related_name="flights",
                                     on_delete=models.PROTECT)
    seat_no = models.ManyToManyField(Seat,
                                related_name="bookings", default=None)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        date_str = self.created.strftime("%Y/%m/%d - ") + self.created.strftime("%H:%M:%S")
        return date_str
    
    def get_absolute_url(self):
        return reverse('booking:booking_detail', args=[self.id])
    
    
