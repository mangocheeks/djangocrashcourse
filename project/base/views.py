from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
# what's called when a url is visited

# rooms = [
#     # dictionary of rooms
#     {'id': 1, 'name': 'Let\'s learn python!'},
#     {'id': 2, 'name': 'Design room'},
#     {'id': 3, 'name': 'Front end'},
# ]


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
        # attempts to relogin by manually changing url are redirected to home

    # attempting login
    if request.method == 'POST':
        # username = request.POST.get('username').lower()
        email = request.POST.get('email')
        password = request.POST.get('password').lower()

        try:
            # switched to email
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User does not exist")

        user = authenticate (request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password incorrect")
            
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    # deletes session token to logout user
    logout(request)
    return redirect('home')

def registerPage(request):
    
    form = MyUserCreationForm()

    if request.method=='POST':
        form = MyUserCreationForm(request.POST)
        # capture info from form on submit 
        if form.is_valid():
            user = form.save(commit = False)
            # set false to get immediate access to created user and clean data before adding
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})

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
    room_messages = Message.objects.filter(Q(room__name__icontains=q))
    topics = Topic.objects.all()[0:5] 
    # see only top 5 topics
    room_count = rooms.count()
    # instead of passing through request, rooms can also be accesssed through context dictionairy
    context = {'rooms':rooms, 'topics':topics, 'room_count': room_count, 'room_messages': room_messages}

    return render(request, 'base/home.html', context)
    #return HttpResponse('HomePage')

# gets pk variable from urls.py
def room(request, pk):
    # room = None
    # for i in rooms:
    #     if i['id'] == int(pk):
    #         room = i
    room = Room.objects.get(id=pk)
    participants = room.participants.all()
        # all for many to many
    room_messages = room.message_set.all()
        # set all for many to one
    # get set of message models related to room

    # comment submitted:
    if request.method == 'POST':
        
        message = Message.objects.create(
            # creates instance of message model
            user=request.user,
            room=room,
            # note that it gets body because text was named body in the room.html
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)


    # context is a dictionary that assigns params to pass in
    # first item is in quotations
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    #pass room dictionary item into context to be accessible in room.html
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context= {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

# user must be logged in to create room, else redirected
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # gets or creates object if not found
        
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # roomform gets prefilled with room value
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        # only allow room editing by host of room
        return HttpResponse('You are not allowed here')

    context = {'form': form, 'topics': topics, 'room':room}

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        # update existing room instead of creating new room
        room.save()
        return redirect('home')

    # check for random syntax errors and auto completes, use large screen
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        # only allow room editing by host of room
        return HttpResponse('You are not allowed here')

# if delete is pressed
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    context = {'obj': room}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        # only allow room editing by message poster
        return HttpResponse('You are not allowed here')

# if delete is pressed
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    context = {'obj': message}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    context= {'form': form}

    if request.method == 'POST':
        # request.FILES passes pfp submission
        form = UserForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})