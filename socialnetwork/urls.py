
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    # path('', TemplateView.as_view(template_name="home.html")),

    url(r'^notifications/', include('notify.urls', 'notifications')),

    path('events/', include('events.urls')),
    path('messages/', include('chat.urls')),
    
    path('friends/', include('friends.urls')),

    path('' , include('olympus.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls'))
    
]
urlpatternsformedia = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = urlpatterns + urlpatternsformedia