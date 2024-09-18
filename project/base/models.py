from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#db tables here

# create classes to represent tables
# attribute = column
# new row = new instance

#when models are added to a db, make a migration, migrate scripts, register in admin panel

# might need to string wrap classes if referenced after

class Topic(models.Model):
    name = models.CharField(max_length=200)

    # represents class as a string
    # ex: print(myObject.__str__())
    def __str__(self):
        return self.name


#inherits from django model
# auto generates with id starting from 1
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # if topic deleted, keep room just set topic to null
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    # desc can be blank, null allowed, can be blank when submitting form
    description = models.TextField(null = True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    # make new migration after updating db relationship
    # timestamp anytime this table is updated/saved
    updated =models.DateTimeField(auto_now=True)
    #first time db is saved
    created = models.DateTimeField(auto_now_add=True)

    # subclass room determines order
    class Meta:
       ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    

class Message(models.Model):
    # remove all messages if suer is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # many to one relationship
    # foreign key required, multiple msgs cab be associated with one room
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # all messsages delete when room is deleted
    body = models.TextField()

    # timestamp anytime this table is updated/saved
    updated =models.DateTimeField(auto_now=True)

    #first time db is saved
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
       ordering = ['-updated', '-created']
    # this model is always ordered

    def __str__(self):
        return self.body[0:50]
        # print first 50 chars