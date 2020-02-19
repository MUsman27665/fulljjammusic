from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   
   

    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),

    url(r'^profilephotoupdate/(?P<pk>\d+)/$',views.ProfilePhotosUpdate.as_view(success_url='/postlist/')),
    
    url(r'^updateprofile/(?P<pk>\d+)/$',views.ProfileUpdateView.as_view(success_url='/postlist/')),
    url(r'^hobbiesandinterests/(?P<pk>\d+)/$',views.HobbiesAndInterestsUpdateView.as_view(success_url='/postlist/')),
    url(r'^educationhistory/(?P<pk>\d+)/$',views.EducationsHistoryUpdate.as_view(success_url='/postlist/')),
    url(r'^emplyementhistory/(?P<pk>\d+)/$',views.EmplyementHistoryUpdate.as_view(success_url='/postlist/')),
    url(r'^aboutprofile/(?P<pk>\d+)/$',views.MultipleModelView.as_view()),
   
   
   
    


    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
     name='password_reset_complete'),
]