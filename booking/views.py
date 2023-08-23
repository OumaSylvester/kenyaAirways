from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import  Aeroplane, Schedule,Time, Route, TypeOfTrip, Passenger, Booking as booking_table
from .forms import SearchForm, PassengerForm, MpesaContactForm
from datetime import datetime
from django.db.models import Count, Q
from .bookings import Booking
from .tasks import payment_completed
from django_daraja.mpesa.core import MpesaClient
import json


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
            # seat_class = cd['seat_class']
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
                                    time_data = {"time_id": time.id, "dep_time": time.dep_time, "arrival_time": time.arrival_time, "aeroplane_id": plane.id, 'plane_no': plane.number_plate}
                                    time_data['price_a'] = route.price_A
                                    time_data['price_b'] = route.price_B
                                    time_data['price_c'] = route.price_C
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
                            route_data.append({"dates": {"dep_date": schedule.dep_date, "arrival_date": schedule.arrival_date}, "id": schedule.id, "times": times})  
                
                        
                    else:
                        route_data.append({"dates": {"dep_date": schedule.dep_date, "arrival_date": schedule.arrival_date}, "id": schedule.id, "times": times})
                       
                               
            route = get_object_or_404(Route, origin=origin, dest=dest)
            booking.add_route(route.id, origin, dest)
            # add travellers to session
            travellers = {'adult': adults, 'youth': youths, 'child': children, 'infant': infants}
            booking.add_travellers(travellers, total_passengers)
            
            return render(request, 
                            'choose_flight.html',
                            {'schedules': route_data, 'origin': origin, 'dest': dest, 'dep_date': dep_date, 'travellers': travellers, 'total_travellers': total_passengers})
    
    return render(request, 
                  'search_flight.html',
                   {'form': form})
             

@csrf_exempt
@require_POST
def add_flight_details_to_session_view(request):
    booking = Booking(request)
    if request.method == 'POST':
        
        data = json.loads(request.body)
        print("Data: ", data['seat_class'])
        booking.add_flight_details(data['schedule_id'], data['time_id'], data['seat_class'])    
        # add type of flight. This should be determined by the window the user chooses
        # By default its one Way
        booking.add_type_of_trip(2) 
        print("Booking details: ", booking.booking['schedule'])
    return redirect('booking:add_passenger')



def add_passenger_view(request):
    booking = Booking(request)
    if request.method == 'POST':
        form = PassengerForm(request.POST)
        print("Booking details: ", booking.booking['schedule'], booking.booking['time'], booking.booking['travellers'])
        if form.is_valid():
            email = form.cleaned_data.get('email')
            passenger = Passenger.objects.filter(email=email)
            if passenger:
                passenger = passenger[0]
                print('I found this passenger ', passenger.email)
            else:
                passenger = form.save()
                print('I am crearing this passenger ', passenger.email)
            booking.add_passenger(passenger.id)
            print("Booking details: ", booking.booking['schedule'], booking.booking['time'], booking.booking['travellers'])
            route = Route.objects.get(id=booking.booking['route'])
            schedule = Schedule.objects.get(id=booking.booking['schedule'])
            time = Time.objects.get(id=booking.booking['time'])
            type_of_trip = TypeOfTrip.objects.get(id=booking.booking['type_of_trip'])
            #  Create booking
            user_booking = booking_table.objects.create(customer=passenger,
                                         adults = booking.booking['travellers']['adult'],
                                         youths=booking.booking['travellers']['youth'],
                                         children = booking.booking['travellers']['child'],
                                         infants = booking.booking['travellers']['infant'],
                                         route = route,
                                         schedule = schedule,
                                         time = time,
                                         type_of_trip = type_of_trip,
                                         cost = booking.get_total_cost(booking.booking['route'])
                                         )
            
            booking.add_booking(user_booking.id)
            payment_completed(user_booking.id, passenger.id)
        return redirect('booking:payment')
        # form = MpesaContactForm()
        # return render(request, 'mpesa-contact.html', {'form': form})
    
            
    else:
        print("Booking details: ", booking.booking['schedule'], booking.booking['time'], booking.booking['travellers']['adult'])
        form = PassengerForm()
        return render(request, 
                      'passenger_form.html',
                      {'form': form})




def mpesa_payment_view(request):
    booking_session = Booking(request)
    # id = booking_session.booking.get('id')
    # booking = get_object_or_404(booking_table,  id=id)
    if request.method == 'POST':
        form = MpesaContactForm(request.POST)
        if form.is_valid():
            cl = MpesaClient()
            phone_number = form.cleaned_data.get('number')
            amount = int(booking_session.get_total_cost(booking_session.booking['route']))
            account_reference = 'Blue Flights'
            transaction_desc = 'Blue Flights Booking'
            callback_url = 'https://api.darajambili.com/express-payment'
           
            response = cl.stk_push(phone_number, 1, account_reference, transaction_desc, callback_url)

            return HttpResponse(response.text) 
    else:
         form = MpesaContactForm()
         return render(request, 'mpesa-contact.html', {'form': form})
               


    



