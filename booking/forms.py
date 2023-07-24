# Create search form, passengers detaisl form, payment details form, 
from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from .models import Flight, FlightClass


def validate_dep_date(value):
    """Customer can only book a flight 3 hrs before departure
    Others things to consider: You can only book upto some period ahead, ...
    """
    from_ = datetime.now() + timedelta(hours=3)
    if value < from_:
        raise ValidationError("%(value)s departure time  must be ateleast 3 hrs ahead of the booking", params={'value': value})

class SearchForm(forms.Form):
    origin = forms.ChoiceField(Flight.objects.values_list('origin').all(), required=True)
    to = forms.ChoiceField(choices=Flight.objects.values_list('dest'), required=True)
    dep_date = forms.DateField(required=True, validators=[validate_dep_date])
    adults = forms.IntegerField(required=True, initial=1, min_value=0, max_value=300)
    youths = forms.IntegerField(required=True, initial=1, min_value=0, max_value=300)
    children = forms.IntegerField(required=True, initial=1, min_value=0, max_value=300)
    infants = forms.IntegerField(required=True, initial=1, min_value=0, max_value=300)
    class_ = forms.ChoiceField(required=False, choices=FlightClass.objects.values_list('class_name'))

    
