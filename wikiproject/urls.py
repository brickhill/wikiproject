from django.contrib import admin
from django.urls import path, include
from .views import home, about

urlpatterns = [
    path('', home, name="home"),
    path('admin/', admin.site.urls),
    path('about', about, name="about")
    # path("", include("myapp.urls")),

]
