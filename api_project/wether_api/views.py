from django.shortcuts import render, redirect
import requests
from datetime import datetime
from .models import City
from .forms import CityForm 
from . import forms



# Create your views here.
def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=cc8cfe443b5d2d93bd0c9964fcde1703'
    
    err_msg = ''
    message = ''
    message_class = ''
    
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
            
                else:
                    err_msg = 'City does NOT exists in the world '

                
            else:
                err_msg = 'City already exists in the database '
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'
    

        

    form = CityForm()

    x = datetime.now()
    
    
    
    cities = City.objects.all()
    

    
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()
        
        

        city_weather = {
            'city' : city.name,
            'datetime' : x,
            'temprature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
            'country' :r['sys']['country']
            
            }

        weather_data.append(city_weather)

    

    context ={
             'weather_data' : weather_data,
             'form' : form,
             'message' : message,
             'message_class' : message_class,
             }
    return render(request, 'home.html', context,)

def delete_city(request, city_name):

    pc = City.objects.get(name=city_name)
    pc.delete()

    return redirect('home')
