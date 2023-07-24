from django.shortcuts import render
from .models import Flight, Aeroplane


def seach_flight_view(request):
    flights = {}
    if 'origin' in request.GET and 'dest' in request.GET  and 'dep_date' in request.GET \
        and 'adults' in request.GET and 'youths' in request.GET and 'children' in request.GET \
        and 'infants' in request.GET:
        origin = request.GET['origin']
        dest = request.GET['dest']
        dep_date = request.GET['dep_date']
        adults = request.GET['adults']
        youths = request.GET['youths']
        children = request.GET['children']
        infants = request.GET['infants']

        total_passengers = adults + youths + children
        
        # Todo
        """"
            Get the schedules for the origin and dest
            get the aeroplane
            get the sits in the aeroplane
            get the number of empty sits in the aeroplane
            compare the number with total passengers. 
            Recomend if greater than total pass
            
        """
        aeroplanes = Aeroplane.objects.filter(empty_sits__gte = total_passengers).values_list('id')
        flights = Flight.objects.filter(origin=origin, dest=dest, schedules__aeroplane__id__in = aeroplanes)
        # Check flight for dep_date only
        flights_on_dep_date = flights.filter(schedules__dep_date=dep_date).all() # confirm return values of above command and this one
        if(flights_on_dep_date):
            flights = flights_on_dep_date
        else:
            flights = flights.all()

        return render(request, 
                        'choose_flight.html',
                        {'flights': flights})
    
    return render(request, 
                  'search_flights.html')
        
        # Todo: Recommend flights if there are no flights on dep_date



