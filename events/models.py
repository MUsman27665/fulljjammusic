from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.shortcuts import Http404,reverse
#This is the Post model
class Events(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=True, null=True)
    event_type = models.CharField(max_length=255,blank=True, null=True)
    event_name = models.CharField(max_length=255,blank=True, null=True)
    event_location = models.CharField(max_length=255,blank=True, null=True)
    event_date = models.CharField(max_length=10,null=True, blank=True)
    event_time = models.TimeField(auto_now=False, auto_now_add=False,max_length=10,null=True, blank=True)
    event_time_type = models.CharField(max_length=10,null=True, blank=True)
    event_time_zone = models.CharField(max_length=10,null=True, blank=True)
    event_description = models.CharField(max_length=255,blank=True, null=True)
    event_invitation = models.ManyToManyField(UserProfile, related_name="event_invitation", blank=True)