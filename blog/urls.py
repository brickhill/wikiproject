from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
    path('series/<slug:slug>/', views.series_detail, name='series_detail'),
    path('search/', views.search, name='search'),

]

