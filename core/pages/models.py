from datetime import date, datetime
from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
from pytz import timezone

# Create your models here.

#Custom user model
class User(AbstractUser):
    email=models.EmailField(max_length=300,unique=True)
    fullname=models.CharField(max_length=500)

    def __str__(self):
        return self.username

#Post model
class Post(models.Model):
    title=models.CharField(max_length=500,unique=True)
    content=models.CharField(max_length=2000)
    postedby=models.ForeignKey(User,on_delete=models.CASCADE)
    likes=models.ManyToManyField(User,related_name="likes",blank=True)
    create_date=models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

#Comment models
class Comment(models.Model):
    commentedby=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    content=models.CharField(max_length=2000)
    def __str__(self):
        return self.content

#Room model
class Room(models.Model):
    user=models.ManyToManyField(User,related_name="user",blank=True)

#Message model
class Message(models.Model):
    room=models.ForeignKey(Room,on_delete=models.CASCADE)
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.CharField(max_length=4000)