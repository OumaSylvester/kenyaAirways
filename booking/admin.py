from django.contrib import admin
from .models import Route,Time, Schedule,TypeOfTrip, SeatClass, Passenger,Aeroplane,Seat, Booking


class SeatInline(admin.TabularInline):
    model=Seat
    extra = 1

class AeroplaneAdmin(admin.ModelAdmin):
    inlines = [SeatInline]

class AeroplaneInline(admin.TabularInline):
    model = Aeroplane
    extra = 1

class RouteAdmin(admin.ModelAdmin):
    inlines =[AeroplaneInline]

admin.site.register(Route,RouteAdmin)

admin.site.register(Aeroplane, AeroplaneAdmin)
admin.site.register([Time, Schedule,TypeOfTrip, SeatClass, Passenger, Seat, Booking])
