# Create search form, passengers detaisl form, payment details form, 
from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from .models import Route, SeatClass, Passenger





cities_qset = Route.objects.values_list('origin').distinct()
cities = []
for c in cities_qset:
    city = c[0]
    cities.append((city, city))

class_qset = SeatClass.objects.values_list('class_name')
classes = []
for c in class_qset:
    class_ = c[0]
    classes.append((class_, class_))


def validate_dep_date(value):
    """Customer can only book a flight 3 hrs before departure
    Others things to consider: You can only book upto some period ahead, ...
    """
    from_ = datetime.now() + timedelta(hours=3)
    from_ = from_.date()
    if value < from_:
        raise ValidationError("%(value)s departure time  must be at least 3 hrs ahead of the booking", params={'value': value})
class SearchForm(forms.Form):
    origin = forms.ChoiceField(choices = cities, widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'aria-label': 'Select Departure City'})) 
    to = forms.ChoiceField(choices=cities, widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'aria-label': 'Select Departure City'}))
    dep_date = forms.DateField(required=True, validators=[validate_dep_date], initial=datetime.today().date(), 
                               widget=forms.DateInput(attrs={'class': 'form-select form-select-lg', 'aria-label': 'Select Destination City', 'type': 'date',
                                                             'value': datetime.today().date(), 'min': datetime.today().date(), 'max': datetime.today().date() + timedelta(days=90)} ))
    adults = forms.IntegerField(required=True, min_value=0, max_value=10,
                                 widget=forms.NumberInput(attrs={'class': 'form-control', 'aria-label': 'Number of adults', 'value': 1}))
    youths = forms.IntegerField(required=True, min_value=0, max_value=10,
                                 widget=forms.NumberInput(attrs={'class': 'form-control', 'aria-label': 'Number of youths', 'value': 0}))
    children = forms.IntegerField(required=True, min_value=0, max_value=10,
                                   widget=forms.NumberInput(attrs={'class': 'form-control', 'aria-label': 'Number of children', 'value': 0}))
    infants = forms.IntegerField(required=True, min_value=0, max_value=10, 
                                 widget=forms.NumberInput(attrs={'class': 'form-control', 'aria-label': 'Number of infants', 'value': 0}))
    seat_class = forms.ChoiceField(required=False, choices=classes, widget=forms.Select(attrs={'class': 'form-select form-select-lg', 'aria-label': 'Select Class'}))


class PassengerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            
    class Meta:
        model = Passenger
        fields = ['first_name', 'last_name',
                   'email', 'telephone', 'national_id', 'passport_id']
        


class MpesaContactForm(forms.Form):
    number = forms.CharField(
        max_length=12,
        strip=True,
        label='Mpesa Number',
         required=True,
         widget=forms.NumberInput(attrs={'class': 'form-control', 'aria-label': 'Number of infants', 'placeholder': '0712345678'}))

    
