from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
# from .admin import admin_site

from courses.mentor_admin import mentor_admin_site


urlpatterns = [
    path('mentor-admin/', mentor_admin_site.urls),
    path('admin/', admin.site.urls),  
    # path('admin1/', admin_site.urls),

    path('api/auth/', include('authentication.urls')),
    path('accounts/', include('allauth.urls')),
    path('courses/', include('courses.urls')),
    path('api/chat/', include('chat.urls')), 
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




