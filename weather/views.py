from django.shortcuts import render,redirect
import requests
from .models import City
from .forms import CityForm
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def index(request):
    far_weather=[('celcius','Celcius'),('farenheit','Farenheit')]
    url1 = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=98e6745c3682b89eacc6c65fe2409f6e'
    url='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=98e6745c3682b89eacc6c65fe2409f6e'
    city='delhi'

    err_msg=''
    message=''
    message_class=''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count=City.objects.filter(name=new_city).count()

            if existing_city_count==0:
                r=requests.get(url.format(new_city)).json()
                print(r)
                if r['cod']==200:

                    form.save()
                else:
                    err_msg='City doesnt exists in world'
            else:
                err_msg='City is already exist'
        if err_msg:
            message=err_msg
            message_class='is-danger'
        else:
            message='City added successfully'
            message_class='is-success'


    print(err_msg)
    form = CityForm()



    cities=City.objects.all()
    weather_data=[]

    for city in cities:


        r=requests.get(url.format(city)).json()

        city_weather={
        'city':city.name,
        'temperature':r['main']['temp'] ,
        'description':r['weather'][0]['description'] ,
        'icon':r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)



    print(weather_data)
    context={
        'weather_data':weather_data,
        'form':form,
        'message':message,
        'message_class':message_class
    }
    return render(request,'weather/weather.html',context)

def delete_city(request,city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')


def contact(request):
    if request.method=='POST':
        message=request.POST['message']
        email=request.POST['name']

        send_mail(email,message,settings.EMAIL_HOST_USER,['abhisheka063@gmail.com'],fail_silently=False)
    return render(request,'weather/index.html')


def unit(request):
    unit=request.GET.get('celcius','default')
    print(unit)
        #url1 = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=98e6745c3682b89eacc6c65fe2409f6e'
    #url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=98e6745c3682b89eacc6c65fe2409f6e'

    url1 = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=98e6745c3682b89eacc6c65fe2409f6e'


    return render(request,'weather/weather.html')

def about(request):
    return render(request,'weather/about.html')