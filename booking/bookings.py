from django.conf import settings
from .models import Route, SeatClass, Schedule, Time


class Booking():
    def __init__(self, request) -> None:
        self.session = request.session
        booking = self.session.get(settings.BOOKING_SESSION_ID)
        if not booking:
            booking = self.session[settings.BOOKING_SESSION_ID] = {}
        self.booking = booking

    def save(self):
        self.session.modified = True


    def add_route(self, route_id, origin, dest):
        self.booking['route'] = route_id
        self.booking['origin'] = origin
        self.booking['dest'] = dest
        self.save()
    def add_flight_details(self, schedule_id, time_id, seat_class):
      
        date = Schedule.objects.get(id = schedule_id)
        time = Time.objects.get(id=time_id)
        

        self.booking['date'] = date.dep_date.strftime("%Y/%m/%d")
        self.booking['dep_time'] = time.dep_time.strftime("%H:%M %p")
        # seat_class_obj = SeatClass.objects.get(class_name=seat_class)
        
         # For security reasons u might pass the date, time and class_. Then read db for the the same insted of sending id
        # to frontend
        self.booking['seat_class'] = seat_class
        self.booking['schedule'] = schedule_id
        self.booking['time'] = time_id
        self.save()


    # def add_ui_details(dep_date, ):
        # bad design....i guess


    
    def add_passenger(self, passenger_id):
        self.booking['passenger'] = passenger_id

    def add_travellers(self, travellers: dict, total_travellers):
        self.booking['travellers'] = travellers
        self.booking['total_travellers'] = total_travellers
        self.save()

    def add_type_of_trip(self, type_of_trip_id):
        self.booking['type_of_trip'] = type_of_trip_id
        self.save()

    def add_booking(self, booking_id):
        self.booking['id'] = booking_id
        self.save()

    def get_total_cost(self, route):
        seat_class = self.booking['seat_class']
        route_obj = Route.objects.get(id=route)
        column_name = ''
        price = 0
        if seat_class == "Class A Executive":
            price = route_obj.price_A
            # column_name = 'price_A'
        elif seat_class == "Class B Middle":
            price = route_obj.price_B
            # column_name = 'price_B'
        elif seat_class == "Class C Lower":
            price = route_obj.price_C
            # column_name = 'price_C'
        # Get the flight price for a single client
        
        
        # Get total travellers for the booking
        # This not the best way to get the total travellers. map?...
        total_travellers = 0
        for value in self.booking['travellers'].values():
            total_travellers += value
        return total_travellers * price
    
  

    
    
    
    