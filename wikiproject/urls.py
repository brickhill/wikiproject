from django.contrib import admin
from django.urls import path, include
from .views import home, about,register

urlpatterns = [
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path('about', about, name="about"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),

    # path("", include("myapp.urls")),

]
