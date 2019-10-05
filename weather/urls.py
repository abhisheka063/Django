
from django.urls import path
from .import views


urlpatterns = [

    path('',views.index,name='home'),
    path('/delete/<city_name>/',views.delete_city,name='delete_city'),
    path('contact/',views.contact,name='contact'),
    path('/unit/',views.unit,name='unit'),
    path('about/',views.about,name='about')

]
