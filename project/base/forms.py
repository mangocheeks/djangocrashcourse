from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields= '__all__'
        # creates form inputs based on form metadata
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        # specify fields
        model = User
        fields = ['username', 'email']