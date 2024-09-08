#generate custom urls file specific to each app
from django.urls import path
from . import views


urlpatterns =[
    #when someone goes to home page (empty url) , trigger home function from views.py to return an http reponse
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
]