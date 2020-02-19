from django.shortcuts import Http404,reverse,render,redirect,get_object_or_404,HttpResponse,HttpResponseRedirect,render_to_response
from django.contrib.auth.models import User,auth #auth will use as a login part 
from django.contrib import messages
from .models import UserPost,UserComment,PostLike,UserProfile,FavPagePostUserComment,UserFavouritePages,FavouritePages,FavPagePost
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import DeleteView,TemplateView,RedirectView
import subprocess 
from datetime import date
from chat.models import Thread
import datetime
#import birthday
from django.conf import settings
from friends.models import FriendRequest
from django.db.models import Q
# Create your views here.
# @method_decorator(login_required, name='dispatch')






def showprofile(request):
    return render(request,'posts.html')

def home(request):
    return redirect('/accounts/register/')


# @method_decorator(login_required, name='dispatch')
class PostCreate(CreateView):
    model = UserPost
    fields = ['post_subject','post_write','post_image','post_video']
    def form_valid(self, form):
        self.object = form.save()
        self.object.uploaded_by = self.request.user.userprofile
        self.object.save()
        for friend in self.object.uploaded_by.friends.all():
            verb_before = " Uploaded a new Post on profile"
            verb = verb_before
            friend.user.notifications.create(verb=verb, actor_text=self.request.user.userprofile.username)
        return redirect('/postlist/')

def markread(request):
    request.user.notifications.update(read=True)
    return redirect('/postlist/')

class postcreatenewsfeed(CreateView):
    model = UserPost
    fields = ['post_subject','post_write','post_image','post_video']
    def form_valid(self, form):
        self.object = form.save()
        self.object.uploaded_by = self.request.user.userprofile
        self.object.save()
        for friend in self.object.uploaded_by.friends.all():
            verb_before = " Shared a New Post"
            verb = verb_before
            friend.user.notifications.create(verb=verb, actor_text=self.request.user.userprofile.username)
        return redirect('/newsfeeds/')

class FavPagePostCreate(CreateView):
    model = FavPagePost  
    fields = ['post_subject','post_write','post_image','post_video']
    def form_valid(self, form):
        page = get_object_or_404(FavouritePages, pk=self.kwargs['pk'])
        self.object = form.save()
        self.object.uploaded_by = self.request.user.userprofile
        self.object.fav_page = page
        self.object.save()
        for page_member in page.fav_page_members.all():
            verb_before = " Uploaded a new Post in "
            verb_post = page.fav_page_name
            verb = verb_before+verb_post
            page_member.notifications.create(verb=verb, actor_text=self.request.user.userprofile.username)
        return redirect(page.get_absolute_url())
        #return redirect(page.get_absolute_url()) #, pk=page_id#)

class PostUpdate(UpdateView):
    model = UserPost
    template_name='olympus/userpost_update_form.html'
    fields = ['post_subject','post_write','post_image','post_video']
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(PostUpdate, self).get_object()
        if not obj.uploaded_by == self.request.user.userprofile:
            raise Http404
        return obj  


class FavpagePostUpdate(UpdateView):
    model = FavPagePost
    template_name='olympus/favpagepost_update_form.html'
    fields = ['post_subject','post_write','post_image','post_video']
    def form_valid(self, form):
        post = get_object_or_404(FavPagePost, pk=self.kwargs['pk'])
        page = post.fav_page
        self.object = form.save()
        self.object.save()
        return redirect('favpageposts', pk = page.id) 


def FavpagePostDelete(request, pk):
    fav_page_post = get_object_or_404(FavPagePost, pk=pk)
    if fav_page_post.uploaded_by == request.user.userprofile:
        fav_page_post.delete()
    return redirect('favpageposts',pk=fav_page_post.fav_page.pk)    

class ViewForMembers(TemplateView):
    template_name = 'olympus/members.html'
    def get_context_data(self, **kwargs):
        context = super(ViewForMembers, self).get_context_data(**kwargs)
        context['all_users']=UserProfile.objects.all()
        context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
        context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
        context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
        context['friends_list_p']= self.request.user.userprofile.friends.all()
        return context

class PostDelete(DeleteView):
    model = UserPost
    #used this method to not confirm just delete (not post just delete and get)
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    
    #template_name='olympus/userpost_form.html'
    
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(PostDelete, self).get_object()
        if not obj.uploaded_by == self.request.user.userprofile:
            raise Http404
        return obj  


class CommentCreate(CreateView):
    model = UserComment
    # template_name='olympus/newsfeeds.html'
    fields = ['comment','c_image']
    def form_valid(self, form):
        mypost = get_object_or_404(UserPost, pk=self.kwargs['pk'])
        self.object = form.save()
        self.object.comment_by = self.request.user.userprofile
        #self.object.post_owner = mypost.uploaded_by
        self.object.post = mypost
        self.object.save()
        verb_before = " Commmented on your "
        verb_post = mypost.post_write
        verb_after = " post"
        verb=verb_before+verb_post+verb_after
        mypost.uploaded_by.user.notifications.create(verb=verb, actor_text=self.request.user.userprofile.username)
        return HttpResponseRedirect(mypost.get_absolute_url())
        # return HttpResponseRedirect('')
        #return redirect('postdetails', pk = mypost.pk)

class FavpagepostCommentCreate(CreateView):
    model = FavPagePostUserComment
    # template_name='olympus/newsfeeds.html'
    fields = ['comment','c_image']
    def form_valid(self, form):
        mypost = get_object_or_404(FavPagePost, pk=self.kwargs['pk'])
        page = get_object_or_404(FavouritePages, pk = mypost.fav_page.id)
        self.object = form.save()
        self.object.comment_by = self.request.user.userprofile
        #self.object.post_owner = mypost.uploaded_by
        self.object.post = mypost
        self.object.save()
        verb_before = " Commmented on your post in "
        verb_page = page.fav_page_name
        verb_after = " Favourtie Page's "
        verb_post = mypost.post_write
        verb=verb_before+verb_page+verb_after+verb_post
        mypost.uploaded_by.user.notifications.create(verb=verb, actor_text=self.request.user.userprofile.username)
        return HttpResponseRedirect(page.get_absolute_url())


def CommentDelete(request, pk):
    comment = get_object_or_404(UserComment, pk=pk)
    if comment.comment_by == request.user.userprofile:
        comment.delete()
    return redirect('postdetails',pk=comment.post.pk)

def favpagepostCommentDelete(request, pk):
    comment = get_object_or_404(FavPagePostUserComment, pk=pk)
    if comment.comment_by == request.user.userprofile:
        comment.delete()
    return redirect('favpagepostdetails',pk=comment.post.pk)

class UpdateCommentView(UpdateView):
    model = UserComment
    fields = ['comment','c_image']
    def form_valid(self, form):
        mypost = get_object_or_404(UserPost, pk=self.kwargs['pk'])
        self.object = form.save()
        self.object.comment_by = self.request.user.userprofile
        #self.object.post_owner = mypost.uploaded_by
        self.object.post = mypost
        self.object.save()
        return redirect('postdetails', pk = mypost.pk)

class FavpagepostUpdateCommentView(UpdateView):
    model = FavPagePostUserComment
    fields = ['comment','c_image']
    def form_valid(self, form):
        mypost = get_object_or_404(FavPagePost, pk=self.kwargs['pk'])
        self.object = form.save()
        self.object.comment_by = self.request.user.userprofile
        #self.object.post_owner = mypost.uploaded_by
        self.object.post = mypost
        self.object.save()
        return redirect('favpagepostdetails', pk = mypost.pk)

def myfavouritepages(request,pk):
    people = UserProfile.objects.filter(id=pk).first()
    rec_friend_requests = FriendRequest.objects.filter(to_user=people).order_by('-id')
    context={
        'people':UserProfile.objects.filter(id=pk).first(),
        'fav_pages': FavouritePages.objects.filter(fav_page_members=request.user).all(),
        'friends_list_p': request.user.userprofile.friends.all(),
        'rec_friend_requests': rec_friend_requests
        }
    context['msg_list'] = Thread.objects.filter(first_id=request.user.id).order_by('-timestamp')
    context['unread_notifs'] = request.user.notifications.filter(recipient=request.user)
    template_name = 'olympus/MyFavouritePages.html'
    return render(request, template_name, context)

def musicandplaylist(request, pk):
    people = UserProfile.objects.filter(id=pk).first()
    rec_friend_requests = FriendRequest.objects.filter(to_user=people).order_by('-id')
    context={
        'people':UserProfile.objects.filter(id=pk).first(),
        'fav_pages':UserFavouritePages.objects.filter(user=request.user).all(),
        'friends_list_p': request.user.userprofile.friends.all(),
        'rec_friend_requests': rec_friend_requests
        }
    context['msg_list'] = Thread.objects.filter(first_id=request.user.id).order_by('-timestamp')
    context['unread_notifs'] = request.user.notifications.filter(recipient=request.user)
    template_name = 'olympus/MusicAndPlaylist.html'
    return render(request, template_name, context)

class CommentUpdate(UpdateView):
    model = UserPost
    template_name='olympus/usercomment_update_form.html'
    fields = ['comment','c_image']

class MultipleModelViewForProfilePosts(TemplateView):
    template_name = 'olympus/userpost_form.html'

    def get_context_data(self, **kwargs):

         context = super(MultipleModelViewForProfilePosts, self).get_context_data(**kwargs)
         context['friends_list_p'] = self.request.user.userprofile.friends.all()
         context['all_posts'] = UserPost.objects.filter(uploaded_by=self.request.user.userprofile).order_by('-post_cr_date')
         context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
         context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
         context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
        #  context['likes'] = PostLike.objects.all()
         return context

class MultipleModelViewForFavPagePosts(TemplateView):
    template_name = 'olympus/favpagepost_form.html'

    def get_context_data(self, **kwargs):
         page = get_object_or_404(FavouritePages, pk=self.kwargs['pk'])
         context = super(MultipleModelViewForFavPagePosts, self).get_context_data(**kwargs)
         context['friends_list_p'] = self.request.user.userprofile.friends.all()
         context['fav_page_posts'] = FavPagePost.objects.filter(fav_page=page).order_by('-post_cr_date')
         #context['all_posts']=FavPagePost.objects.filter(uploaded_by__friends=self.request.user.userprofile).order_by('-id')
         #context['fav_page_members'] = FavouritePages.objects.all()
         context['page'] = page
         context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
         context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
         #context['user_fav_pages'] = UserFavouritePages.objects.filter(user=self.request.user)
         context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
        #  context['likes'] = PostLike.objects.all()
         return context


class MultipleModelViewForPostdetails(TemplateView):
    template_name = 'olympus/post_details.html'
    def get_context_data(self, **kwargs):
        context = super(MultipleModelViewForPostdetails, self).get_context_data(**kwargs)
        mypost = get_object_or_404(UserPost, pk=self.kwargs['pk'])
        context['friends_list_p'] = self.request.user.userprofile.friends.all()
        context['post'] = mypost
        context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
        context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
        context['all_comments'] = UserComment.objects.filter(post=mypost).order_by('-id')
        context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
        return context

class MultipleModelViewForFavpagePostdetails(TemplateView):
    template_name = 'olympus/favpage_postdetails.html'
    def get_context_data(self, **kwargs):
        context = super(MultipleModelViewForFavpagePostdetails, self).get_context_data(**kwargs)
        mypost = get_object_or_404(FavPagePost, pk=self.kwargs['pk'])
        context['friends_list_p'] = self.request.user.userprofile.friends.all()
        context['post'] = mypost
        context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
        context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
        context['all_comments'] = FavPagePostUserComment.objects.filter(post=mypost).order_by('-id')
        context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
        return context


class MultipleModelViewForProfilePhotos(TemplateView):
    template_name = 'olympus/photos.html'
    def get_context_data(self, **kwargs):
         context = super(MultipleModelViewForProfilePhotos, self).get_context_data(**kwargs)
         #mypost = get_object_or_404(UserPost, pk=self.kwargs['pk'])
         #people = UserProfile.objects.filter(id=id).first()
         context['all_posts'] = UserPost.objects.filter(uploaded_by=self.request.user.userprofile).order_by('-post_cr_date')
         context['friends_list_p'] = self.request.user.userprofile.friends.all()
         context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
         context['unread_notifs'] = self.request.user.notifications.filter(recipient=request.user)
         context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
         #context['all_comments'] = UserComment.objects.filter(post=mypost).order_by('-id')
         return context

class MultipleModelViewForProfilevideos(TemplateView):
    template_name = 'olympus/videos.html'
    def get_context_data(self, **kwargs):
         context = super(MultipleModelViewForProfilevideos, self).get_context_data(**kwargs)
         #mypost = get_object_or_404(UserPost, pk=self.kwargs['pk'])
        #  def getLength(post_video):
        #      result = subprocess.Popen(["ffprobe", post_video],stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
        #      context['duration'] = [x for x in result.stdout.readlines() if x.decode()]
         context['all_posts'] = UserPost.objects.filter(uploaded_by=self.request.user.userprofile).order_by('-post_cr_date')
         context['friends_list_p'] = self.request.user.userprofile.friends.all()
         context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
         context['unread_notifs'] = self.request.user.notifications.filter(recipient=request.user)
         context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
         #context['all_comments'] = UserComment.objects.filter(post=mypost).order_by('-id')
         return context

# def post_details(request,pk):
#     post = get_object_or_404(UserPost,pk=pk)
#     comments = UserComment.objects.filter(post=post).order_by('-id')
#     context = {
#         'post': post,
#         'all_comments': comments
#     }
#     return render(request,'olympus/post_details.html',context)

def addtofavpages(request, pk):
    page = get_object_or_404(FavouritePages, id=pk)
    page.fav_page_members.add(request.user)
    user_id = request.user.userprofile.id
    return redirect('myfavouritepages', pk=user_id)

def leavefavpage(request, pk):
    page = get_object_or_404(FavouritePages, id=pk)
    page.fav_page_members.remove(request.user)
    user_id = request.user.userprofile.id
    return redirect('myfavouritepages', pk=user_id)

class MultipleModelViewForFeeds(TemplateView):
    template_name = 'olympus/newsfeeds.html'
    def get_context_data(self, **kwargs):
        context = super(MultipleModelViewForFeeds, self).get_context_data(**kwargs)
        context['all_posts']=UserPost.objects.filter(uploaded_by__friends=self.request.user.userprofile).order_by('-id')
        context['inuser'] = UserPost.objects.filter(uploaded_by=self.request.user.userprofile)
        context['friends_list_p'] = self.request.user.userprofile.friends.all()
        context['fav_pages'] = FavouritePages.objects.filter(~Q(fav_page_members=self.request.user)).all()
        #context['birthday_alert'] = UserProfile.objects.get_birthdays()
        context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp') 
        context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
        context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
        context['all_peoples']= UserProfile.objects.all()[:3]
        return context

def favouritepagecreate(request):
    context={
        'friends_list_p': request.user.userprofile.friends.all()
        }
    context['unread_notifs'] = request.user.notifications.filter(recipient=request.user)
    context['msg_list'] = Thread.objects.filter(first_id=request.user.id).order_by('-timestamp') 
    context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=request.user.userprofile).order_by('-id')
    template_name = 'olympus/favpagecreate.html'
    return render(request, template_name, context)

def get_success_url(self):
    return reverse ('postdetails', kwargs={'pk': self.object.parent.pk})

def like_postinpro(request,pk):
    post = get_object_or_404(UserPost, pk=pk)
    is_liked =False 
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked=False
    else:
        post.likes.add(request.user)
        is_liked=True
        verb = " Liked your post"
        post.uploaded_by.user.notifications.create(verb=verb, actor_text=request.user.userprofile.username)
    return redirect('/postlist/')

def like_postinPeoplePro(request,id):
    post = get_object_or_404(UserPost, id=id)
    is_liked =False 
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked=False
    else:
        post.likes.add(request.user)
        is_liked=True
        verb = " Liked your post"
        post.uploaded_by.user.notifications.create(verb=verb, actor_text=request.user.userprofile.username)

    return redirect('showresult',id=post.uploaded_by.id)

def like_post(request,pk):
    post = get_object_or_404(UserPost, pk=pk)
    is_liked =False 
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked=False
    else:
        post.likes.add(request.user)
        is_liked=True
        verb = " Liked your post"
        post.uploaded_by.user.notifications.create(verb=verb, actor_text=request.user.userprofile.username)
    return redirect('/newsfeeds/')
    # return HttpResponseRedirect('/postdetails/{}/')
 
def likefavpagepost(request, pk):
    favpagepost = get_object_or_404(FavPagePost, pk=pk)
    page = get_object_or_404(FavouritePages, pk=favpagepost.fav_page.id)
    is_liked =False 
    if favpagepost.likes.filter(id=request.user.id).exists(): #favpage_likes=favpage_post_likes
        favpagepost.likes.remove(request.user)
        is_liked=False
    else:
        favpagepost.likes.add(request.user)
        is_liked=True
        verb_before = "Liked your post in the "
        verb_page = page.fav_page_name
        verb_after = " Favourtie Page"
        verb=verb_before+verb_page+verb_after
        favpagepost.uploaded_by.user.notifications.create(verb=verb, actor_text=request.user.userprofile.username)
    return redirect(page.get_absolute_url())


def like_postindv(request,pk):
    post = get_object_or_404(UserPost, pk=pk)
    is_liked =False 
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked=False
    else:
        post.likes.add(request.user)
        is_liked=True
        verb = " Liked your post"
        post.uploaded_by.user.notifications.create(verb=verb, actor_text=request.user.userprofile.username)
    return redirect(post.get_absolute_url())

def likefavpagepostindv(request,pk):
    post = get_object_or_404(FavPagePost, pk=pk)
    is_liked =False 
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked=False
    else:
        post.likes.add(request.user)
        is_liked=True
        verb_before = "Liked your post in the "
        verb_page = post.fav_page.fav_page_name
        verb_after = " Favourtie Page"
        verb=verb_before+verb_page+verb_after
        post.uploaded_by.user.notifications.create(verb=verb, actor_text=request.user.userprofile.username)
    return HttpResponseRedirect('favpagepostdetails', pk=post.fav_page.id)
    #return redirect('postdetails',pk=post.pk)

def like_comment(request,pk):
    comment = get_object_or_404(UserComment, pk=pk)
    is_liked =False
    if comment.cm_likes.filter(id=request.user.id).exists():
        comment.cm_likes.remove(request.user)
        is_liked=False
    else:
        comment.cm_likes.add(request.user)
        is_liked=True
        verb_before = " Liked your comment in the "
        verb_post = comment.post.post_write+" Post"
        verb=verb_before+verb_post
        comment.comment_by.user.notifications.create(verb=verb, actor_text=request.user.userprofile.username)
    return redirect('postdetails',pk=comment.post.id)

def likefavpagepostcomment(request, pk):
    comment = get_object_or_404(FavPagePostUserComment, pk=pk)
    is_liked =False
    if comment.cm_likes.filter(id=request.user.id).exists():
        comment.cm_likes.remove(request.user)
        is_liked=False
    else:
        comment.cm_likes.add(request.user)
        is_liked=True
        verb_before = " Liked your comment in the "
        verb_page = comment.post.fav_page.fav_page_name
        verb_after = " Favourtie Page's "
        verb_post = comment.post.post_write+" Post"
        verb=verb_before+verb_page+verb_after+verb_post
        comment.comment_by.user.notifications.create(verb=verb, actor_text=request.user.userprofile.username)
    #post = get_object_or_404(UserPost,pk=pk)
    return redirect('favpagepostdetails',pk=comment.post.id)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class PostLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        # slug = self.kwargs.get("slug")
        post = get_object_or_404(UserPost, pk=pk)
        updated = False
        liked = False
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            liked = True
            post.likes.add(request.user)        
        updated = True
        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data)

        


        
# def liking(request, pk):
#     userpost = get_object_or_404(UserPost, pk=pk)
#     obj = PostLike.objects.all()
#     if obj.user.filter(id=request.user.userprofile.id).exists():
#         print('user already exists which likes this')
#         obj.user.delete()
#     else:
#         print('user likes this')
#         newlike = PostLike.objects.create(user=request.user.userprofile, post=userpost)
#     return redirect('/postlist/')


