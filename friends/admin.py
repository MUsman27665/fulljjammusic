from django.contrib import admin

from .models import FriendRequest, FriendGroup, FriendGroupPost,FGroupPostLike,FGroupPostComment

class FriendsAdmin(admin.ModelAdmin):
    list_display = ('to_user', 'from_user', 'timestamp')
admin.site.register(FriendRequest, FriendsAdmin)

class FriendGroupAdmin(admin.ModelAdmin):
    list_display = ('FGroup_name', 'FGroup_desc', 'FGroup_admin', 'FGroup_cr_date')
admin.site.register(FriendGroup, FriendGroupAdmin)

class FriendGroupPostAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'post_write',
    'post_image','post_video','post_cr_date')
admin.site.register(FriendGroupPost, FriendGroupPostAdmin)

class FGroupPostLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'FGroup_post', 'FGroup_com_cr_date')
admin.site.register(FGroupPostLike, FGroupPostLikeAdmin)

class FGroupPostCommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'comment_by','comment','c_image','cm_cr_date')
admin.site.register(FGroupPostComment, FGroupPostCommentAdmin)

