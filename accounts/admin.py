from django.contrib import admin
from .models import UserProfile,HobbiesAndInterests,EducationHistory,EmplyementHistory,ProfilePhotos

admin.site.register(UserProfile)
admin.site.register(HobbiesAndInterests)
admin.site.register(EducationHistory)
admin.site.register(EmplyementHistory)
admin.site.register(ProfilePhotos)