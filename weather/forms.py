from django import forms
from django.forms import TextInput
from .models import City

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name' : TextInput(attrs={'class' : 'input','placeholder':'Search City/State/Country'})}
