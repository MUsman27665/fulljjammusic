from django.urls import path, re_path
from . import views

app_name = 'chat'
urlpatterns = [
    path("", views.InboxView.as_view()),
    re_path(r"^(?P<username>[\w.@+-]+)", views.ThreadView.as_view()),
]
