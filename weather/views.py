import requests
from django.shortcuts import render, redirect
from .models import City
from . import forms
# Create your views here.


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=bce656c0013538b220967b7c409f516a'
    err_msg = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = forms.CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "No Such City exists : "+new_city
                    message_class = 'is-danger'
            else:
                err_msg = 'City Already exists in Database'
                message_class = 'is-warning'


        if err_msg:
            message = err_msg
        #    message_class = 'is-danger'
        else:
            message = 'City Added Successfully'
            message_class = 'is-success'
    print(err_msg)
    form = forms.CityForm()

    cities =  City.objects.all()
    weather_date = []
    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
        'city':city.name,
        'temperature': r['main']['temp'],
        'description':r['weather'][0]['description'],
        'icon':r['weather'][0]['icon']
        }
        weather_date.append(city_weather)

    context = {
        'weather':weather_date,
        'form':form,
        'message':message,
        'message_class':message_class
        }
    return render(request,'weather/weather.html',context)



def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
