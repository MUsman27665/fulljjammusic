from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.shortcuts import Http404,reverse


class FriendRequest(models.Model):
    to_user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='to_user')
    from_user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='from_user')
    timestamp = models.DateTimeField(auto_now_add= True)

class FriendGroup(models.Model):
    FGroup_name = models.CharField(max_length=255, null=False,blank=False)
    FGroup_desc = models.TextField(blank=True, null=False)
    FGroup_admin = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='group_admin')
    FGroup_members = models.ManyToManyField(User,related_name='peoples',blank =True)
    FGroup_img = models.ImageField(upload_to='pics/fgroups',blank=True, null=True)
    FGroup_cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s" % self.FGroup_name

    def get_absolute_url(self):
        return reverse('fgroupPosts', kwargs={'pk':self.pk})

class FriendGroupPost(models.Model): 
    post_subject = models.CharField(max_length=255,blank=True, null=True)
    uploaded_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=True, null=True)
    post_write =models.TextField(max_length=255,blank=True, null=True)
    post_image = models.ImageField(upload_to='pics/fgroups_content', null=True, blank=True)
    post_video = models.FileField(upload_to='videos/fgroups_content',blank=True, null=True)
    post_cr_date = models.DateTimeField(auto_now_add=True)
    FGroup = models.ForeignKey(FriendGroup, on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User,related_name='fgroup_post_likes',blank =True)

    def __str__(self):
         return "%s" % self.uploaded_by

    def get_absolute_url(self):
        return reverse('fgroupPostdetails',kwargs={'pk':self.pk})

class FGroupPostLike(models.Model):
    FGroup_post = models.ForeignKey(FriendGroupPost,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE) 
    FGroup_com_cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
         return "%s" % self.liked_by

class FGroupPostComment(models.Model):
    post =  models.ForeignKey(FriendGroupPost,on_delete=models.CASCADE, null=True, blank=True)
    #post_owner =  models.ForeignKey(UserProfile,on_delete=models.CASCADE, null=True, blank=True)
    comment_by =  models.ForeignKey(UserProfile,on_delete=models.CASCADE, null=True, blank=True)
    comment =  models.TextField(blank=True, null=True)
    c_image =  models.ImageField(upload_to='pics/fgroups_content', null=True, blank=True)
    cm_cr_date =  models.DateTimeField(auto_now_add=True)
    cm_likes = models.ManyToManyField(User,related_name='fgroup_cm_likes',blank =True)
    def __str__(self):
         return "%s" % self.comment_by

    def get_absolute_url(self):
        return reverse('fgroup_posts',kwargs={'pk':self.pk})