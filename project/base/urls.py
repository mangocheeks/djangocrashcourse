#generate custom urls file specific to each app
from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns =[
    #when someone goes to home page (empty url) , trigger home function from views.py to return an http reponse
    path('', views.home, name="home"),
    path('room/', views.room, name="room"),
]