import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

# Create the index request with the API call and and our cities var containing all the cities from the db

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=b9f82f3a364c3fddf1ff4bfd1b085a4c'
    cities = City.objects.all()


    # code below used for checking db for city and/or if the api returns a value for that city when entering a new city
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
                    err_msg = 'City does not exist!'
            else: 
                err_msg = 'City already exists in the database!'
 
        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    form = CityForm()

    # empty array to store data, iterate over all cities in the db, request that weather data from the api

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    print (weather_data)

    context = {
        'weather_data': weather_data, 
        'form' : form,
        'message' : message,
        'message_class' : message_class,
        }
    return render(request, 'weather/weather.html', context)

# function to delete a city from the db

def delete_city(request, city_name):

    City.objects.get(name=city_name).delete()
    return redirect('home')