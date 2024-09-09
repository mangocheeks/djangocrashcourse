from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm
# Create your views here.
# what's called when a url is visited

# rooms = [
#     # dictionary of rooms
#     {'id': 1, 'name': 'Let\'s learn python!'},
#     {'id': 2, 'name': 'Design room'},
#     {'id': 3, 'name': 'Front end'},
# ]
def home(request):
    # get all rooms in room database, overwrites predfined room dictionary
    rooms = Room.objects.all()
    # instead of passing through request, rooms can also be accesssed through context dictionairy
    # context = {'rooms': rooms}
    return render(request, 'base/home.html', {'rooms':rooms})
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