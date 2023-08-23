from django.urls import path
from .views import seach_flight_view, add_flight_details_to_session_view, add_passenger_view, mpesa_payment_view

app_name = 'booking'
urlpatterns = [
    path('', seach_flight_view, name='search_flight'),
    path('flight_details/', add_flight_details_to_session_view, name='add_flight_details'),
    path('passenger/', add_passenger_view, name='add_passenger'),
    path('payment/', mpesa_payment_view, name="payment"),    
]