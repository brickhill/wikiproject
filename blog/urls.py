from django.urls import path
from . import views
# MAJOR Mail list.

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/<str:series>', views.post_detail,
         name='post_detail2'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
    path('std/<slug:keyword>/', views.page_std_detail, name='page_std'),
    path('series/<slug:slug>/', views.series_detail, name='series_detail'),
    path('search/', views.search, name='search'),
]
