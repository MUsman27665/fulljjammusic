from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.shortcuts import Http404,reverse
#This is the Post model

class FavouritePages(models.Model):
    fav_page_name = models.TextField(blank=False, null=False)
    fav_page_desc = models.TextField(blank=True, null=False)
    fva_page_img = models.ImageField(upload_to='pics/fav_page_img/',blank=True, null=True)
    fav_page_owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    fav_page_cr_date = models.DateTimeField(auto_now_add=True)
    fav_page_members = models.ManyToManyField(User,related_name='fav_page_members', blank=True)
    def __str__(self):
        return "%s" % self.fav_page_name

    def get_absolute_url(self):
        return reverse('favpageposts', kwargs={'pk':self.pk})

class UserPost(models.Model):
    post_subject = models.CharField(max_length=255,blank=True, null=True)
    uploaded_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=True, null=True)
    post_write =models.TextField(max_length=255,blank=True, null=True)
    post_image = models.ImageField(upload_to='pics', null=True, blank=True)
    post_video = models.FileField(upload_to='videos',blank=True, null=True)
    post_cr_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='likes',blank =True)
    def __str__(self):
         return "%s" % self.post_write

    def get_absolute_url(self):
        return reverse('postdetails',kwargs={'pk':self.pk})

class FavPagePost(models.Model):
    post_subject = models.CharField(max_length=255,blank=True, null=True)
    uploaded_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE,blank=True, null=True)
    post_write =models.TextField(max_length=255,blank=True, null=True)
    post_image = models.ImageField(upload_to='pics/fav_pages_content', null=True, blank=True)
    post_video = models.FileField(upload_to='videos/fav_pages_content',blank=True, null=True)
    post_cr_date = models.DateTimeField(auto_now_add=True)
    fav_page = models.ForeignKey(FavouritePages, on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ManyToManyField(User,related_name='favpage_likes',blank =True)
    # Above name is equals to favpage_post_likes
    comments = models.ManyToManyField(User, related_name='favpage_post_comments', blank=True)
    
    def __str__(self):
         return "%s" % self.uploaded_by

    def get_absolute_url(self):
        return reverse('favpageposts',kwargs={'pk':self.pk})

class PostLike(models.Model):
    post = models.ForeignKey(UserPost,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE) 
    cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
         return "%s" % self.liked_by

class FavPagePostLike(models.Model):
    post = models.ForeignKey(FavPagePost,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE) 
    favpage_com_cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
         return "%s" % self.liked_by

class UserComment(models.Model):
    post =  models.ForeignKey(UserPost,on_delete=models.CASCADE, null=True, blank=True)
    #post_owner =  models.ForeignKey(UserProfile,on_delete=models.CASCADE, null=True, blank=True)
    comment_by =  models.ForeignKey(UserProfile,on_delete=models.CASCADE, null=True, blank=True)
    comment =  models.TextField(blank=True, null=True)
    c_image =  models.ImageField(upload_to='pics', null=True, blank=True)
    cm_cr_date =  models.DateTimeField(auto_now_add=True)
    cm_likes = models.ManyToManyField(User,related_name='cm_likes',blank =True)
    def __str__(self):
         return "%s" % self.comment

    def get_absolute_url(self):
        return reverse('postdetails',kwargs={'pk':self.pk})

class FavPagePostUserComment(models.Model):
    post =  models.ForeignKey(FavPagePost,on_delete=models.CASCADE, null=True, blank=True)
    #post_owner =  models.ForeignKey(UserProfile,on_delete=models.CASCADE, null=True, blank=True)
    comment_by =  models.ForeignKey(UserProfile,on_delete=models.CASCADE, null=True, blank=True)
    comment =  models.TextField(blank=True, null=True)
    c_image =  models.ImageField(upload_to='pics/fav_pages_content', null=True, blank=True)
    cm_cr_date =  models.DateTimeField(auto_now_add=True)
    cm_likes = models.ManyToManyField(User,related_name='favpage_cm_likes',blank =True)
    def __str__(self):
         return "%s" % self.comment_by

    def get_absolute_url(self):
        return reverse('favpageposts',kwargs={'pk':self.pk})



class UserFavouritePages(models.Model):
    fav_page_id = models.ForeignKey(FavouritePages, on_delete=models.CASCADE, null=True, blank=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    