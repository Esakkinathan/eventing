from django import forms
from django.forms import ModelForm
from .models import Venue,Events
#Create a venue form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields=('name','address','zip_code','phonenumber','web','email_address','venue_image')
        labels = {
            'name':'',
            'address':'',
            'zip_code':'',
            'phonenumber':'',
            'web':'',
            "email_address":'',
            "venue_image":''
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Venue Name'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Address'}),
            'zip_code':forms.TextInput(attrs={'class':'form-control','placeholder':'Zip_Codes'}),
            'phonenumber':forms.NumberInput(attrs={'class':'form-control','placeholder':'Phone Number'}),
            'web':forms.URLInput(attrs={'class':'form-control','placeholder':'Web Address'}),
            "email_address":forms.EmailInput(attrs={'class':'form-control','placeholder':'Email Address'})
        }
#event superuser admin form
class EventsFormAdmin(ModelForm):
    class Meta:
        model = Events
        fields={'name','event_date','venue','manager','attendees','description'}
        labels = {
            'name':'',
            'event_date':'YYYY-MM-DD HH:MM:SS',
            'venue':'Add venue',
            'manager':'Manager',
            'attendees':'Attendees',
            "description":''
        }
        widgets={
            "name":forms.TextInput(attrs={'class':'form-control','placeholder':'Event Name'}),
            "event_date":forms.DateTimeInput(attrs={'class':'form-control','placeholder':'Event Date'}),
            "venue":forms.Select(attrs={'class':'form-control form-select','placeholder':'Venue Name'}),
            "manager":forms.Select(attrs={'class':'form-control form-select','placeholder':'Manager Name'}),
            "attendees":forms.SelectMultiple(attrs={'class':'form-control','placeholder':'Attendees'}),
            "description":forms.Textarea(attrs={'class':'form-control','placeholder':'Description'}),        
        }
class EventsForm(ModelForm):
    class Meta:
        model = Events
        fields={'name','event_date','venue','attendees','description'}
        labels = {
            'name':'',
            'event_date':'YYYY-MM-DD HH:MM:SS',
            'venue':'Add venue',
            'attendees':'Attendees',
            "description":''
        }
        widgets={
            "name":forms.TextInput(attrs={'class':'form-control','placeholder':'Event Name'}),
            "event_date":forms.DateTimeInput(attrs={'class':'form-control','placeholder':'Event Date'}),
            "venue":forms.Select(attrs={'class':'form-control form-select','placeholder':'Venue Name'}),
            "attendees":forms.SelectMultiple(attrs={'class':'form-control','placeholder':'Attendees'}),
            "description":forms.Textarea(attrs={'class':'form-control','placeholder':'Description'}),        
        }