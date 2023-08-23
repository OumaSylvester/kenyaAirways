from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render
from ..models import  Aeroplane, Schedule
from ..forms import SearchForm
from datetime import datetime
from django.db.models import Count, Q
from ..bookings import Booking


def seach_flight_view(request):
    form = SearchForm()
    booking = Booking(request)
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            origin = cd['origin']
            dest = cd['to']
            dep_date = cd['dep_date']
            seat_class = cd['seat_class']
            adults = cd['adults']
            youths = cd['youths']
            children = cd['children']
            infants = cd['infants']
            
            total_passengers = adults + youths + children
            
            
            # Get aeroplanes with enough seats
            aeroplanes = Aeroplane.objects.filter(seats__available=True, route__origin=origin, route__dest=dest).annotate(available_seats=Count('seats', filter=Q(seats__available=True)))
            planes_with_enough_seats = aeroplanes.filter(available_seats__gte=total_passengers)
            # Get schedules for the search criteria
            schedules = Schedule.objects.filter(dep_date__gte=datetime.today(),  routes__origin=origin, routes__dest=dest).distinct()\
                .order_by("dep_date", "times__dep_time")
            
            route_data = []
            times = []
            for schedule in schedules:                        
                for route in schedule.routes.all():
                    if route.origin == origin and route.dest == dest:
                       
                        times = []
                        for time in schedule.times.all().distinct():
                            # Append the available seat for each seat class for the allocated plane for the respetive time
                            for plane in time.aeroplanes.filter(id__in=route.aeroplanes.all().values_list("id")):
                                if plane in planes_with_enough_seats.all():
                                    time_data = {"dep_time": time.dep_time, "arrival_time": time.arrival_time, "aeroplane_id": plane.id}
                                    time_data['class_a_exe'] = plane.seats.filter(available=True, seat_class__class_name="Class A - Executive").count()
                                    time_data['class_b_mid'] = plane.seats.filter(available=True, seat_class__class_name="Class B - Middle Class").count()
                                    time_data['class_c_lower'] = plane.seats.filter(available=True, seat_class__class_name="Class C - Lower Class").count()
                                    times.append(time_data)
                # Find out how the duplcates end up in the data. If a date has 2 times, the date is added twice ....3...
                if times:
                    if route_data: # Avoid duplicates
                        found_duplicate = False
                        for date in route_data:
                            if date['dates']['dep_date'] == schedule.dep_date:
                                found_duplicate = True
                                break
                        if not found_duplicate: 
                            route_data.append({"dates": {"dep_date": schedule.dep_date, "arrival_date": schedule.arrival_date}, "times": times})  
                
                        
                    else:
                        route_data.append({"dates": {"dep_date": schedule.dep_date, "arrival_date": schedule.arrival_date}, "times": times})
                       
                               

            
            # add travellers to session
            travellers = {'adults': adults, 'youths': youths, 'children': children, 'infants': infants}
            booking.add_travellers(travellers)

            return Response({'schedules': route_data, 'origin': origin, 'dest': dest, 'total_travellers': total_passengers})
    
    return render(request, 
                  'search_flight.html',
                   {'form': form})
        
        



