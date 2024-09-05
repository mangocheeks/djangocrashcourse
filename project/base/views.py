from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# what's called when a url is visited

def home(request):
    return HttpResponse('HomePage')

def room(request):
    return HttpResponse('Room')