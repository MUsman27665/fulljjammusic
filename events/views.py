from django.shortcuts import Http404,reverse,render,redirect,get_object_or_404,HttpResponse,HttpResponseRedirect,render_to_response
from django.contrib.auth.models import User,auth #auth will use as a login part 
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import DeleteView,TemplateView,RedirectView
import subprocess
from django.conf import settings
from friends.models import FriendRequest
from django.db.models import Q
from .models import Events
# Create your views here.
class eventsview(TemplateView):
    template_name = 'events/events.html'

    def get_context_data(self, **kwargs):
        context = super(eventsview, self).get_context_data(**kwargs)
        context['friends_list_p'] = self.request.user.userprofile.friends.all()
        #context['all_events'] = Events.objects.filter(user=self.request.user.userprofile)
        context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
        context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
        return context

class EventCreate(CreateView):
    model = Events
    fields = ['event_type', 'event_name','event_location','event_date','event_time','event_time_type','event_time_zone','event_description','event_invitation']
    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user.userprofile
        self.object.save()
        return redirect('/events/showevents/')