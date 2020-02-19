from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin
#from notify import Notification
#from Notification import notify
from django.views.generic import DetailView, ListView
from friends.models import FriendRequest



from .forms import ComposeForm
from .models import Thread, ChatMessage, MessageNotification


class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chats/thread.html'
    form_class = ComposeForm
    success_url = './'
    # def get_context_data(self, **kwargs):
    #     #sender = get_object_or_404(User, pk=self.request.user)
    #     context = super(ThreadView, self).get_context_data(**kwargs)
    #     context['friends_list_p'] = self.request.user.userprofile.friends.all()
    #     context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
    #     context['unread_msgs'] = self.unread_messages()
    #     return context

    def unread_messages(self):
        return self.request.user.chatMessage.filter(status=False).count()

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
        context['friends_list_p'] = self.request.user.userprofile.friends.all()
        context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
        context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        #user2 = self.get_object()
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)


