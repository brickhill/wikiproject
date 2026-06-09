from django.contrib import admin
from django.urls import path, include
from .views import home, about, register, member, contact, experiment
from django.conf import settings
from django.conf.urls.static import static
from .views import MyLoginView, MyLogoutView

urlpatterns = [
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path('about', about, name="about"),
    path("accounts/login/",MyLoginView.as_view(),name="login"),
    path("accounts/logout/",MyLogoutView.as_view(),name="logout"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('member/', member, name="member"),
    path('blog/', include('blog.urls')),
    path('page/', include('blog.urls')),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path('cookies/', include('cookie_consent.urls')),
    path('contact/', contact, name='contact'),
    path('experiment/', experiment, name='experiment')

]
if settings.DEBUG:
    print(f"Media: {settings.MEDIA_URL}:{settings.MEDIA_ROOT}")
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
