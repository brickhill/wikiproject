from django.contrib import admin
from django.urls import path, include
from .views import home, about,register, member
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path('about', about, name="about"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('member/', member, name="member"),
    path('blog/', include('blog.urls')),

    path("ckeditor/", include("ckeditor_uploader.urls")),
]


if settings.DEBUG:
    print(f"Media: {settings.MEDIA_URL}:{settings.MEDIA_ROOT}")
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)