from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import User,HobbiesAndInterests,EducationHistory,EmplyementHistory,ProfilePhotos

@receiver(post_save,sender=User)
def save_profile(sender, instance, created, **kwarg):
    if created:
        HobbiesAndInterests.objects.create(user = instance)
        EducationHistory.objects.create(user = instance)
        EmplyementHistory.objects.create(user = instance) 
        ProfilePhotos.objects.create(user = instance)
        # UserProfile.objects.create(user = instance,first_name=instance.first_name,
        #                                 last_name=instance.last_name,username=instance.username)
        