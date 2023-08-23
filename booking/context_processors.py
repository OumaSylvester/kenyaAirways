from .bookings import Booking


def booking(request):
    return {'booking': Booking(request).booking}

