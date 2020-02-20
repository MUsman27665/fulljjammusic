from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.models import User,auth #auth will use as a login part 
from django.contrib import messages
from .forms import UserProfileForm,Userform
from .models import UserProfile,HobbiesAndInterests,EducationHistory,EmplyementHistory,ProfilePhotos
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import DeleteView,TemplateView
from friends.models import FriendRequest
from .models import Thread, ChatMessage, MessageNotification


def register(request):
    registered =False

    if request.method == 'POST':
        user_form = Userform(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.first_name = user.first_name
            profile.last_name = user.last_name
            profile.username = user.username
            profile.save()


            registered=True
            print('PROFILE_CREATED')

        else:
            print(user_form.errors,profile_form.errors)
            print('PROFILE_IS_NOT_CREATED')
            return redirect('/')
    else:
        user_form = Userform()
        profile_form = UserProfileForm()
    return render(request,'01-LandingPage.html')


# def register(request):
#     profile_form = UserProfileForm(request.POST)
#     if request.method=='POST' and profile_form.is_valid():
#         first_name=request.POST['first_name']
#         last_name=request.POST['last_name']
#         username = request.POST['username']
#         email=request.POST['email']
#         password=request.POST['password']
#         #validations
#         if User.objects.filter(username=username).exists():
#             print("This User Name is Already exists.")
#             messages.info(request,'Username_TAKKEN')
#             return redirect('/accounts/register/')
#         elif User.objects.filter(email=email).exists():
#             print("This email is Already exists")
#             messages.info(request,'email_TAKKEN')
#             return redirect('/accounts/register/')
#         else:
#             user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             profile.save()
    
#             print('\nUser created')
#             messages.info(request,'USER_CREATED')
#             return redirect('/')
#     else:
#         print('\nUser not created')
#         print(UserProfileForm.errors)
#         redirect('/accounts/register/')
#     return render(request, "01-LandingPage.html")



def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            print("You are loged in")
            return redirect('/postlist/')
        else:
            print("You are not loged in")
            return redirect('/accounts/login/')
    else:
        return render(request,'01-LandingPage.html')


def logout(request):
    auth.logout(request)
    return redirect('/accounts/login/')



class ProfileUpdateView(UpdateView):
    model = UserProfile
    fields = ['first_name','last_name','username','gender','datetimepicker','p_photo','h_photo','subtitles','political_incline',
            'about_me','birthplace','lives_in','country','province','city','occupation',
            'relationship_status','website','phone_number','religious_belifs','political_incline',
            'facebook','twitter','RSS','dibble','spotify']
    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context['friends_list_p'] = self.request.user.userprofile.friends.all()
        context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
        context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
        context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
        return context

class ProfilePhotosUpdate(UpdateView):
    model = UserProfile
    template_name='mainprofile.html'
    fields = ['p_photo','h_photo']


class HobbiesAndInterestsUpdateView(UpdateView):
    model = HobbiesAndInterests
    template_name='accounts/hobbiesandinterests_form.html'
    fields = ['hobbies','fav_music','fav_tv_shows','fav_books','fav_movies','fav_writers','fav_games','other_interests']
    def get_context_data(self, **kwargs):
        context = super(HobbiesAndInterestsUpdateView, self).get_context_data(**kwargs)
        context['friends_list_p'] = self.request.user.userprofile.friends.all()
        context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
        context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
        context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
        return context

class EducationsHistoryUpdate(UpdateView):
    model = EducationHistory
    template_name='accounts/educationhistory_form.html'
    fields = ['titile_place1','period1','description1','titile_place2','period2','description2','titile_place3','period3','description3']
    def get_context_data(self, **kwargs):
        context = super(EducationsHistoryUpdate, self).get_context_data(**kwargs)
        context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
        context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
        context['friends_list_p'] = self.request.user.userprofile.friends.all()
        context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
        return context


class EmplyementHistoryUpdate(UpdateView):
    model = EmplyementHistory
    template_name='accounts/educationhistory_form.html'
    fields = ['etitile_place1','eperiod1','edescription1','etitile_place2','eperiod2','edescription2','etitile_place3','eperiod3','edescription3']
    def get_context_data(self, **kwargs):
        context = super(EmplyementHistory, self).get_context_data(**kwargs)
        context['friends_list_p'] = self.request.user.userprofile.friends.all()
        context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
        context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
        context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
        return context



class MultipleModelView(TemplateView):
    template_name = 'accounts/aboutprofile.html'

    def get_context_data(self, **kwargs):
         context = super(MultipleModelView, self).get_context_data(**kwargs)
         context['personalinfo'] = UserProfile.objects.all()
         context['hobbies'] = HobbiesAndInterests.objects.all()
         context['education'] = HobbiesAndInterests.objects.all()
         context['emplyement'] = HobbiesAndInterests.objects.all()
         context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
         context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
         context['friends_list_p'] = self.request.user.userprofile.friends.all()
         context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
         return context



# def updateprofile(request,pk):
#     id_post = User.objects.get(id=request.user.id)
#     profile_form = UserProfileForm(request.POST or None,request.FILES or None,instance=id_post)
#     if profile_form.is_valid():
#         profile_form.save()
#         print('profile updated')
#         redirect('/')
#     else:
#         print('profile not updated this is update view')
#         redirect('/accounts/updateprofile/')
#     return render(request,'profileform.html',{'form':profile_form})

# def updateprofile(request):
#     #postuser = get_object_or_404(UserProfile,user=user)
#     profileform = UserProfileForm(request.POST or None, request.FILES or None)
#     if profileform.is_valid():
#         profileform.save()
#         print('/PROFILE CREATED')
#         messages.info(request, 'profile created Succesfully!')
#         return redirect('/accounts/showprofile/')
#     else:
#         print('not edited')
#         return redirect('/')
#     return render(request,'editprofile.html',{'profileform':profileform})


# def showeditprofile(request):
#     profiledata = UserProfile.objects.all()
#     return render(request,'editprofile.html',{ 'profiledata':profiledata})


# def showprofile(request):
#     profiledata = UserProfile.objects.all()
#     postdata = Post.objects.all()
#     return render(request,'posts.html',{ 'profiledata':profiledata,'postdata':postdata})

# def createpost(request):
#     cr_post = PostModelForm(request.POST or None, request.FILES or None)
#     if cr_post.is_valid():
#         cr_post.save()
#         print('/nYou Posted Succesfully')
#         messages.info(request, 'You Posted Succesfully!')
#         return redirect('/accounts/register/')
#     else:
#         print('/Not Posted')
#         messages.info(request, 'Please fill all the information!')
#         redirect('/')
#     return render(request,'postlist.html',{'postform':cr_post})

# def createcomment(request):
#     cr_comment = CommentModelForm(request.POST or None, request.FILES or None)
#     if cr_comment.is_valid():
#         cr_comment.save()
#         print('/nYou Commented Succesfully')
#         messages.info(request, 'You Posted Succesfully!')
#         return redirect('/accounts/showprofile/')
#     else:
#         print('/Not Commented')
#         messages.info(request, 'Please fill all the information!')
#         redirect('/')
#     return render(request,'postlist.html',{'commentform':cr_comment})





