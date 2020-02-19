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
from chat.models import Thread
from django.conf import settings
from accounts.models import UserProfile
from olympus.models import UserPost,UserComment,FavouritePages,FavPagePost
from friends.models import FriendRequest,FriendGroup,FriendGroupPost,FGroupPostLike,FGroupPostComment
from django.db.models import Q

class SearchView(TemplateView):
	template_name = 'friends/search-result.html'
	def get_context_data(self, **kwargs):
		context = super(SearchView, self).get_context_data(**kwargs)
		si = self.request.GET.get('si')
		if si == None:
			si == "There is no result related to this"
		else:
			users = UserProfile.objects.exclude(user=self.request.user).filter(Q(first_name__icontains=si) | Q(last_name__icontains=si) | Q(username__icontains=si))
			context['result_count'] = users.count
			context['users'] = users
			#context['all_posts'] = UserPost.objects.filter(uploaded_by__in=users)
			return context
"""
class FGroupPostCommentCreate(CreateView):
    model = FGroupPostComment
    # template_name='olympus/newsfeeds.html'
    fields = ['comment','c_image']
    def form_valid(self, form):
        mypost = get_object_or_404(FriendGroupPost, pk=self.kwargs['pk'])
        group = get_object_or_404(FriendGroup, pk = mypost.FGroup.id)
        self.object = form.save()
        self.object.comment_by = self.request.user.userprofile
        #self.object.post_owner = mypost.uploaded_by
        self.object.post = mypost
        self.object.save()
        return HttpResponseRedirect(group.get_absolute_url())
"""
class Fgroupcreate(CreateView):
	model = FriendGroup
	fields = ['FGroup_name','FGroup_desc','FGroup_img']
	def form_valid(self, form):
		self.object = form.save()
		self.object.FGroup_admin = self.request.user.userprofile
		self.object.FGroup_members =self.request.user.userprofile
		self.object.save()
		return HttpResponseRedirect('/friends/friendgroups/')


def PeopleProfileView(request,id):
	people = UserProfile.objects.filter(id=id).first()
	rec_friend_requests = FriendRequest.objects.filter(to_user=request.user.userprofile).order_by('-id')
	u = people.user
	friends = people.friends.all()

	# is this user our friend
	button_status = 'none'
	if people not in request.user.userprofile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
	if len(FriendRequest.objects.filter(from_user=request.user.userprofile).filter(to_user=people)) == 1:
		button_status = 'friend_request_sent'

	post = UserPost.objects.filter(uploaded_by=people).order_by('-id')
	friends_list_p = request.user.userprofile.friends.all()
	context = {
		'people':people,'all_posts':post,
		'u': u,
		'button_status': button_status,
		'friends_list': friends,
		'friends_list_p': friends_list_p,
		'rec_friend_requests': rec_friend_requests,
	}
	context['msg_list'] = Thread.objects.filter(first_id=request.user.id).order_by('-timestamp')
	context['unread_notifs'] = request.user.notifications.filter(recipient=request.user)
	return render(request,'friends/people_posts.html',context)



def PeopleProfileAboutView(request,id):
	people = get_object_or_404(UserProfile, id=id)
	rec_friend_requests = FriendRequest.objects.filter(to_user=request.user.userprofile).order_by('-id')
	post = UserPost.objects.filter(uploaded_by=people).order_by('-id')
	friends = people.friends.all()
	button_status = 'none'
	if people not in request.user.userprofile.friends.all():
		button_status = 'not_friend'
	
	context = {
		'people':people,
		'button_status': button_status,
		'friends_list': friends,
		'all_posts':post,
		'friends_list_p': request.user.userprofile.friends.all(),
		'rec_friend_requests': rec_friend_requests,
	}
	context['msg_list'] = Thread.objects.filter(first_id=request.user.id).order_by('-timestamp')
	context['unread_notifs'] = request.user.notifications.filter(recipient=request.user)
	return render(request,'friends/people_about.html',context)

def PeopleProfilePhotoView(request,id):
	people = get_object_or_404(UserProfile, id=id)
	rec_friend_requests = FriendRequest.objects.filter(to_user=request.user.userprofile).order_by('-id')
	post = UserPost.objects.filter(uploaded_by=people).order_by('-id')
	friends = people.friends.all()
	button_status = 'none'
	if people not in request.user.userprofile.friends.all():
		button_status = 'not_friend'
	context = {
		'people':people,
		'button_status': button_status,
		'friends_list': friends,
		'all_posts':post,
		'friends_list_p': request.user.userprofile.friends.all(),
		'rec_friend_requests': rec_friend_requests,
	}
	context['msg_list'] = Thread.objects.filter(first_id=request.user.id).order_by('-timestamp')
	context['unread_notifs'] = request.user.notifications.filter(recipient=request.user)
	return render(request,'friends/people_photo.html',context)

def PeopleProfileVideoView(request,id):
	people = get_object_or_404(UserProfile, id=id)
	rec_friend_requests = FriendRequest.objects.filter(to_user=request.user.userprofile).order_by('-id')
	post = UserPost.objects.filter(uploaded_by=people)
	friends = people.friends.all()
	button_status = 'none'
	if people not in request.user.userprofile.friends.all():
		button_status = 'not_friend'
	context = {
		'people':people,
		'button_status': button_status,
		'friends_list': friends,
		'all_posts':post,
		'friends_list_p': request.user.userprofile.friends.all(),
		'rec_friend_requests': rec_friend_requests,
	}
	context['msg_list'] = Thread.objects.filter(first_id=request.user.id).order_by('-timestamp')
	context['unread_notifs'] = request.user.notifications.filter(recipient=request.user)
	return render(request,'friends/people_video.html',context)

def RecFriendRequestsView(request,id):
	people = UserProfile.objects.filter(id=id).first()
	rec_friend_requests = FriendRequest.objects.filter(to_user=people).order_by('-id')
	count_request = rec_friend_requests.count
	
	context = {
		'count_request':count_request,
		'rec_friend_requests': rec_friend_requests,
		'friends_list_p': request.user.userprofile.friends.all()
	}
	context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
	context['unread_notifs'] = request.user.notifications.filter(recipient=request.user)
	return render(request,'accounts/friend_requests.html',context)


def friends_list(request,id):
	people = UserProfile.objects.filter(id=id).first()
	rec_friend_requests = FriendRequest.objects.filter(to_user=people).order_by('-id')
	button_status = 'none'
	if people not in request.user.userprofile.friends.all():
		button_status = 'not_friend'
	context = {
		'rec_friend_requests':rec_friend_requests,
		'button_status': button_status,
		'friends_list_p': request.user.userprofile.friends.all()
	}
	context['msg_list'] = Thread.objects.filter(first_id=request.user.id).order_by('-timestamp')
	context['unread_notifs'] = request.user.notifications.filter(recipient=request.user)
	return render(request,'accounts/friends_list.html',context)

def friendgroups(request):
	people = UserProfile.objects.filter(id=request.user.userprofile.id).first()
	rec_friend_requests = FriendRequest.objects.filter(to_user=people).order_by('-id')
	context={
		'friends_list_p': request.user.userprofile.friends.all(),
		'fav_pages': FriendGroup.objects.filter(FGroup_members=request.user).all(),
		'rec_friend_requests': rec_friend_requests,

		}
	context['msg_list'] = Thread.objects.filter(first_id=request.user.id).order_by('-timestamp')
	context['unread_notifs'] = request.user.notifications.filter(recipient=request.user)
	template_name = 'FriendGroups.html'
	return render(request, template_name, context)

def communitybadges(request):
	context={
		'friends_list_p':request.user.userprofile.friends.all(),
		'posts': UserPost.objects.filter(uploaded_by=request.user.userprofile), 
		'fav_pages': FavouritePages.objects.filter(fav_page_members=request.user).all(),
		'user_favpage_posts': FavPagePost.objects.filter(uploaded_by=request.user.userprofile).all(),
		'friend_groups': FriendGroup.objects.filter(FGroup_members=request.user).all(),
		'user_fgroup_posts': FriendGroupPost.objects.filter(uploaded_by=request.user.userprofile).all(),
	}
	context['msg_list'] = Thread.objects.filter(first_id=request.user.id).order_by('-timestamp')
	context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=request.user.userprofile).order_by('-id')
	context['unread_notifs'] = request.user.notifications.filter(recipient=request.user)
	template_name= 'communitybadges.html'
	return render(request, template_name, context)

def friends_list_for_people(request,id):
	people = UserProfile.objects.filter(id=id).first()
	rec_friend_requests = FriendRequest.objects.filter(to_user=request.user.userprofile).order_by('-id')
	friends = people.friends.all()
	button_status = 'none'
	if people not in request.user.userprofile.friends.all():
		button_status = 'not_friend'
	context = {
		'people':people,
		'button_status': button_status,
		'friends_list': friends,
		'friends_list_p': request.user.userprofile.friends.all(),
		'rec_friend_requests':rec_friend_requests,
	}
	context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
	context['unread_notifs'] = request.user.notifications.filter(recipient=request.user)
	return render(request,'friends/people_friends.html',context)
def send_friend_request(request, id):
    if request.user.is_authenticated:
        user = get_object_or_404(UserProfile, id=id)
        frequest, created = FriendRequest.objects.get_or_create(from_user=request.user.userprofile,to_user=user)
        return redirect('showresult',id=user.id)

def cancel_friend_request(request, id):
	if request.user.is_authenticated:
		user = get_object_or_404(UserProfile, id=id)
		frequest = FriendRequest.objects.filter(from_user=request.user.userprofile,to_user=user).first()
		frequest.delete()
		return redirect('showresult',id=user.id)

def accept_friend_request(request, id):
	user = UserProfile.objects.filter(id=id).first()
	frequest = FriendRequest.objects.filter(from_user=user, to_user=request.user.userprofile).first()
	user1 = frequest.to_user
	user2 = frequest.from_user
	user1.friends.add(user2)
	user2.friends.add(user1)
	frequest.delete()
	# return redirect('RecFriendRequests',id=user1.id)
	return redirect('showresult',id=user2.id)

def delete_friend_request(request, id):
	from_user = get_object_or_404(UserProfile, id=id)
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user.userprofile).first()
	frequest.delete()
	return HttpResponseRedirect('/friends/RecFriendRequests/{}'.format(request.user.userprofile.id))



def unfriend_user(request, id):
	unfriend_to = UserProfile.objects.filter(id=id).first()
	unfriend_from = request.user.userprofile
	user1 = unfriend_to
	user2 = unfriend_from
	user1.friends.remove(user2)
	user2.friends.remove(user1)
	# return redirect('RecFriendRequests',id=user1.id)
	return redirect('showresult',id=user1.id)


class FGroupPostCreate(CreateView):
	model = FriendGroupPost
	#template_name='friends/friendgrouppost_form.html'
	fields = ['post_subject','post_write','post_image','post_video']
	def form_valid(self, form):
		group = get_object_or_404(FriendGroup, pk=self.kwargs['pk'])
		self.object = form.save()
		self.object.uploaded_by = self.request.user.userprofile
		self.object.FGroup = group
		self.object.save()
		for group_member in group.FGroup_members.all():
			verb_before = " Uploaded a new Post in "
			verb_group =group.FGroup_name
			verb = verb_before + verb_group
			group_member.notifications.create(verb=verb, actor_text=self.request.user.userprofile.username)
		return HttpResponseRedirect('/friends/friendgroups/')
        #return redirect(group.get_absolute_url())
        #return redirect(page.get_absolute_url()) #, pk=page_id#)


class FGroupPostUpdate(UpdateView):
    model = FriendGroupPost
    template_name='friends/friendgrouppost_update_form.html'
    fields = ['post_subject','post_write','post_image','post_video']
    def form_valid(self, form):
        post = get_object_or_404(FriendGroupPost, pk=self.kwargs['pk'])
        group = post.FGroup
        self.object = form.save()
        self.object.save()
        return redirect('fgroupPosts', pk = group.id) 

def FGroupPostDelete(request, pk):
    fgroup_post = get_object_or_404(FriendGroupPost, pk=pk)
    if fgroup_post.uploaded_by == request.user.userprofile:
        fgroup_post.delete()
    return redirect('fgroupPosts',pk=fgroup_post.FGroup.pk) 


class FGroupPostCommentCreate(CreateView):
    model = FGroupPostComment
    # template_name='olympus/newsfeeds.html'
    fields = ['comment','c_image']
    def form_valid(self, form):
        mypost = get_object_or_404(FriendGroupPost, pk=self.kwargs['pk'])
        group = get_object_or_404(FriendGroup, pk = mypost.FGroup.id)
        self.object = form.save()
        self.object.comment_by = self.request.user.userprofile
        #self.object.post_owner = mypost.uploaded_by
        self.object.post = mypost
        self.object.save()
        verb_before = " Commented on your post in "
        verb_after = " Post:- "
        group_name = group.FGroup_name
        verb = verb_before+group_name+verb_after+mypost.post_write
        mypost.uploaded_by.user.notifications.create(verb=verb, actor_text=self.request.user.userprofile.username)
        return HttpResponseRedirect(group.get_absolute_url())

def fGroupPostCommentDelete(request, pk):
    comment = get_object_or_404(FGroupPostComment, pk=pk)
    if comment.comment_by == request.user.userprofile:
        comment.delete()
    return redirect('fgroupPostdetails',pk=comment.post.pk)


class MultipleModelViewForFGroupPosts(TemplateView):
    template_name = 'friends/friendgrouppost_form.html'

    def get_context_data(self, **kwargs):
        group = get_object_or_404(FriendGroup, pk=self.kwargs['pk'])
        context = super(MultipleModelViewForFGroupPosts, self).get_context_data(**kwargs)
        context['friends_list_p'] = self.request.user.userprofile.friends.all()
        context['fgroup_posts'] = FriendGroupPost.objects.filter(FGroup=group).order_by('-post_cr_date')
         #context['all_posts']=FavPagePost.objects.filter(uploaded_by__friends=self.request.user.userprofile).order_by('-id')
         #context['fav_page_members'] = FavouritePages.objects.all()
        context['group'] = group
        context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
        context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
        #context['user_fav_pages'] = UserFavouritePages.objects.filter(user=self.request.user)
        context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
        #  context['likes'] = PostLike.objects.all()
        return context


class MultipleModelViewForFGroupPostdetails(TemplateView):
    template_name = 'friends/fgroup_postdetails.html'
    def get_context_data(self, **kwargs):
        context = super(MultipleModelViewForFGroupPostdetails, self).get_context_data(**kwargs)
        mypost = get_object_or_404(FriendGroupPost, pk=self.kwargs['pk'])
        context['friends_list_p'] = self.request.user.userprofile.friends.all()
        context['post'] = mypost
        context['msg_list'] = Thread.objects.filter(first_id=self.request.user.id).order_by('-timestamp')
        context['unread_notifs'] = self.request.user.notifications.filter(recipient=self.request.user)
        context['all_comments'] = FGroupPostComment.objects.filter(post=mypost).order_by('-id')
        context['rec_friend_requests'] = FriendRequest.objects.filter(to_user=self.request.user.userprofile).order_by('-id')
        return context


def likefgrouppostindv(request,pk):
    post = get_object_or_404(FriendGroupPost, pk=pk)
    is_liked =False 
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked=False
    else:
        post.likes.add(request.user)
        is_liked=True
        verb_before = "Liked your post in the "
        verb_group = post.FGroup.FGroup_name
        verb_after = " Friend Group :- "
        verb=verb_before+verb_group+verb_after+post.post_write+" Post"
        post.uploaded_by.user.notifications.create(verb=verb, actor_text=request.user.userprofile.username)
    return redirect(post.get_absolute_url())

def likefgroupPost(request, pk):
    fgroupPost = get_object_or_404(FriendGroupPost, pk=pk)
    group = get_object_or_404(FriendGroup, pk=fgroupPost.FGroup.id)
    is_liked =False 
    if fgroupPost.likes.filter(id=request.user.id).exists(): #favpage_likes=favpage_post_likes
        fgroupPost.likes.remove(request.user)
        is_liked=False
    else:
        fgroupPost.likes.add(request.user)
        is_liked=True
        verb_before = "Liked your post in the "
        verb_group = group.FGroup_name
        verb_after = " Friend Group :- "
        verb=verb_before+verb_group+verb_after+fgroupPost.post_write+" Post"
        fgroupPost.uploaded_by.user.notifications.create(verb=verb, actor_text=request.user.userprofile.username)
    return redirect(group.get_absolute_url())


def likefgroupPostcomment(request, pk):
    comment = get_object_or_404(FGroupPostComment, pk=pk)
    is_liked =False
    if comment.cm_likes.filter(id=request.user.id).exists():
        comment.cm_likes.remove(request.user)
        is_liked=False
    else:
        comment.cm_likes.add(request.user)
        is_liked=True
        verb_before = " Liked your comment in the "
        verb_page = comment.post.FGroup.FGroup_name
        verb_after = " Friend Group's:- "
        verb_post = comment.post.post_write+" Post"
        verb=verb_before+verb_page+verb_after+verb_post
        comment.comment_by.user.notifications.create(verb=verb, actor_text=request.user.userprofile.username)
    #post = get_object_or_404(UserPost,pk=pk)
    return redirect( 'fgroupPostdetails' ,pk=comment.post.id)




