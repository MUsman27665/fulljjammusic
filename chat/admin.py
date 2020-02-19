from django.contrib import admin


from .models import Thread, ChatMessage,MessageNotification

class ChatMessage(admin.TabularInline):
    model = ChatMessage

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]
    class Meta:
        model = Thread 
class MessageNotificationAdmin(admin.ModelAdmin):
    list_display = ['message','sender', 'receiver']
admin.site.register(MessageNotification, MessageNotificationAdmin)
admin.site.register(Thread, ThreadAdmin)

