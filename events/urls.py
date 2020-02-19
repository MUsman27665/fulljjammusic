from django.urls import path,include
from django.conf.urls import url
from . import views


urlpatterns = [


    path('showevents/',views.eventsview.as_view(),name='showevents'),
    path('eventcreate/',views.EventCreate.as_view(success_url='/showevents/')),
    
 


]