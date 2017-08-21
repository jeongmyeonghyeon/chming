from django.conf.urls import url, include

from config.urls import urls_views, urls_apis

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'', include(urls_views)),
    url(r'^api/', include(urls_apis)),
    url(r'^api/admin/', admin.site.urls),
]

# /static/에 대한 요청을 STATIC_ROOT경로의 파일에서 찾는다
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# /media/에 대한 요청을 MEDIA_ROOT경로의 파일에서 찾는다
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
