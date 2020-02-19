from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    friends = models.ManyToManyField("userprofile", related_name="friends_data", blank=True)

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    

    gender = models.CharField(max_length=10,null=True, blank=True)
    datetimepicker=models.CharField(max_length=10,null=True, blank=True)

    p_photo = models.ImageField(upload_to='pics', null=True, blank=True)
    h_photo = models.ImageField(upload_to='pics', null=True, blank=True)

    subtitles = models.CharField(max_length=20,null=True, blank=True)
    about_me = models.TextField(max_length=200,null=True, blank=True)
    birthplace= models.CharField(max_length=20,null=True, blank=True)
    lives_in = models.CharField(max_length=20,null=True, blank=True)
    country = models.CharField(max_length=20,null=True, blank=True)
    province = models.CharField(max_length=20,null=True, blank=True)
    city = models.CharField(max_length=20,null=True, blank=True)
    occupation = models.CharField(max_length=20,null=True, blank=True)
    relationship_status = models.CharField(max_length=20,null=True, blank=True)
    website = models.CharField(max_length=255,null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    religious_belifs = models.CharField(max_length=20,null=True, blank=True)
    political_incline = models.CharField(max_length=20,null=True, blank=True)
    facebook = models.URLField(max_length=255,null=True, blank=True)
    twitter = models.URLField(max_length=255,null=True, blank=True)
    RSS = models.URLField(max_length=255,null=True, blank=True)
    dibble = models.URLField(max_length=255,null=True, blank=True)
    spotify = models.URLField(max_length=255,null=True, blank=True)
    def __str__(self):
         return "%s" % self.user

class ProfilePhotos(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    p_photo = models.ImageField(upload_to='pics', null=True, blank=True)
    h_photo = models.ImageField(upload_to='pics', null=True, blank=True)
    def __str__(self):
         return "%s" % self.user

class HobbiesAndInterests(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    hobbies = models.TextField(blank=True, null=True)
    fav_music = models.TextField(blank=True, null=True)
    fav_tv_shows = models.TextField(blank=True, null=True)
    fav_books = models.TextField(blank=True, null=True)
    fav_movies = models.TextField(blank=True, null=True)
    fav_writers = models.TextField(blank=True, null=True)
    fav_games = models.TextField(blank=True, null=True)
    other_interests = models.TextField(blank=True, null=True)

    def __str__(self):
         return "%s" % self.user
    def get_hobbies_url(self):
    	return "/accounts//accounts/hobbiesandinterests/{}/".format(self.id)
    # def get_hobbies_url(self):
    #     return reverse('postdetails',kwargs={'pk':self.pk})

class EducationHistory(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    titile_place1 = models.TextField(blank=True, null=True)
    period1 = models.TextField(blank=True, null=True)
    description1 = models.TextField(blank=True, null=True)
    titile_place2 = models.TextField(blank=True, null=True)
    period2 = models.TextField(blank=True, null=True)
    description2 = models.TextField(blank=True, null=True)
    titile_place3 = models.TextField(blank=True, null=True)
    period3 = models.TextField(blank=True, null=True)
    description3 = models.TextField(blank=True, null=True)

    def __str__(self):
         return "%s" % self.user


class EmplyementHistory(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True)
    etitile_place1 = models.TextField(blank=True, null=True)
    eperiod1 = models.TextField(blank=True, null=True)
    edescription1 = models.TextField(blank=True, null=True)
    etitile_place2 = models.TextField(blank=True, null=True)
    eperiod2 = models.TextField(blank=True, null=True)
    edescription2 = models.TextField(blank=True, null=True)
    etitile_place3 = models.TextField(blank=True, null=True)
    eperiod3 = models.TextField(blank=True, null=True)
    edescription3 = models.TextField(blank=True, null=True)

    def __str__(self):
         return "%s" % self.user




# class UserPost():
#     pass

# #This is the Post model
# class Post(models.Model):
#     user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    
#     post_write=models.TextField(blank=True, null=True)
#     post_image= models.ImageField(upload_to='pics', null=True, blank=True)
#     #post_cr_date = models.DateTimeField(auto_now_add=True,blank=True)

#     def __str__(self):
#          return self.user.post_write
    
# #This is the Comment model
# class Comment(models.Model):
#     c_post = models.ForeignKey(Post,on_delete=models.CASCADE)
#     comment_by = models.ForeignKey(to=User,on_delete=models.CASCADE)
#     comment_text=models.TextField(blank=True, null=True)
#     comment_image= models.ImageField(upload_to='pics', null=True, blank=True)
#     #comment_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#          return self.user.comment_text
