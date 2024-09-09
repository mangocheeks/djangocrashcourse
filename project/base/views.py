from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
# Create your views here.
# what's called when a url is visited

# rooms = [
#     # dictionary of rooms
#     {'id': 1, 'name': 'Let\'s learn python!'},
#     {'id': 2, 'name': 'Design room'},
#     {'id': 3, 'name': 'Front end'},
# ]


def loginPage(request):
    # attempting login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate (request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password incorrect")
    context = {}
    return render(request, 'base/login_register.html', context)

def home(request):
    # get all rooms in room database, overwrites predfined room dictionary using all()

    # shows all rooms when no q is set
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        # double underscore
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )
    # filters case insensitive as long as q contains chars of topic

    topics = Topic.objects.all()
    room_count = rooms.count()
    # instead of passing through request, rooms can also be accesssed through context dictionairy
    # context = {'rooms': rooms}
    return render(request, 'base/home.html', {'rooms':rooms, 'topics':topics, 'room_count': room_count})
    #return HttpResponse('HomePage')

# gets pk variable from urls.py
def room(request, pk):
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i

    room = Room.objects.get(id=pk)
    # context is a dictionary that assigns params to pass in
    # first item is in quotations
    context = {'room': room}
    #pass room dictionary item into context to be accessible in room.html
    return render(request, 'base/room.html', context)


def createRoom(request):
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # roomform gets prefilled with room value
    form = RoomForm(instance=room)

    context = {'form': form}

    if request.method == 'POST':
        # update existing room instead of creating new room
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    # check for random syntax errors and auto completes, use large screen
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

# if delete is pressed
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    context = {'obj': room}
    return render(request, 'base/delete.html', context)