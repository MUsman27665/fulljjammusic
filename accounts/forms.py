from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class Userform(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('first_name','last_name','username','email','password')


class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('gender','datetimepicker')
            
            


# class PostModelForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['post_write','post_image','user']

# class CommentModelForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['c_post','comment_by','comment_text']
