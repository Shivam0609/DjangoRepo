import requests
from django.shortcuts import render, redirect
from .models import City
from . import forms

from datetime import datetime, timezone


from django.contrib import messages
# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=bce656c0013538b220967b7c409f516a'

    if request.method == 'POST':
        form = forms.CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name'].lower()
            # print(request.POST["name"])
            # print(new_city)
            #new_city = requests.get(url.format(new_city)).json()['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            #existing_city_name = requests.get(url.format(new_city)).json()['name']
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    new_form = form.save(commit=False)
                    new_form.name = new_city
                    new_form.save()

                    # form.save()
                    messages.success(request, "Your search filtered successfully")
                    return redirect(request.path)
                else:
                    messages.warning(request, "No results found for : {}".format(new_city))
                    return redirect(request.path)
            else:
                messages.info(request, "Search result already exists, Scroll down to check if not visible")
                return redirect(request.path)


        # if err_msg:
        #     messages.error(request, err_msg)
        # else:
        #     messages.error(request, 'lease supply valid city name')

    form = forms.CityForm()

    cities =  City.objects.all()
    weather_date = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        dt_epoch = r["dt"]
        sunrise_epoch = r["sys"]["sunrise"]
        sunset_epoch = r["sys"]["sunset"]
        dt = datetime.fromtimestamp(dt_epoch).strftime('%Y-%m-%d %H:%M:%S %p')
        sunrise = datetime.fromtimestamp(sunrise_epoch).strftime('%Y-%m-%d %H:%M:%S %p')
        sunset = datetime.fromtimestamp(sunset_epoch).strftime('%Y-%m-%d %H:%M:%S %p')

        city_weather = {
        'city':city.name,
        'temperature': r['main']['temp'],
        'description':r['weather'][0]['description'],
        'icon':r['weather'][0]['icon'],
        'weather_id': r['weather'][0]['id'],
        'temp_min' : r["main"]["temp_min"],
        'temp_max' : r["main"]["temp_max"],
        'sunrise' : sunrise,
        'sunset' : sunset
        }
        weather_date.append(city_weather)
        # print(city_weather["temperature"],city_weather["temp_min"],city_weather["temp_max"])

    context = {
        'weather':weather_date,
        'form':form
        }
    return render(request,'weather/weather.html',context)



def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
