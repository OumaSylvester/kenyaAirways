from django.urls import path
from .views import seach_flight_view
app_name = 'booking'
urlpatterns = [
    path('', seach_flight_view, name='search_flight')
]