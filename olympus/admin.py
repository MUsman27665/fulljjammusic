
from django.contrib import admin
from .models import UserPost,PostLike,UserComment,FavouritePages,UserFavouritePages,FavPagePost,FavPagePostLike,FavPagePostUserComment

class PostAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'post_write', 'post_image','post_cr_date')
admin.site.register(UserPost, PostAdmin)

class FavPageAdmin(admin.ModelAdmin):
    list_display = ('fav_page_name', 'fav_page_owner', 'fav_page_cr_date')
admin.site.register(FavouritePages, FavPageAdmin)

class FavPagePostAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'post_write',
    'post_image','post_video','post_cr_date')
admin.site.register(FavPagePost, FavPagePostAdmin)

class UserFavPageAdmin(admin.ModelAdmin):
    list_display = ('fav_page_id', 'user')
admin.site.register(UserFavouritePages, UserFavPageAdmin)

class LikedAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'cr_date')
admin.site.register(PostLike, LikedAdmin)

class FavPagePostLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'favpage_com_cr_date')
admin.site.register(FavPagePostLike, FavPagePostLikeAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'comment_by','comment','c_image','cm_cr_date')
admin.site.register(UserComment, CommentAdmin)

class FavPagePostUserCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'comment_by','comment','c_image','cm_cr_date')
admin.site.register(FavPagePostUserComment, FavPagePostUserCommentAdmin)
# admin.site.register(UserComment)
# Register your models here.


