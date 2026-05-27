from django.urls import path
from . import views
# MAJOR Mail list.
# TODO Slug doesn't work on PA for category or series.

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/<str:source>', views.post_detail, name='post_detail2'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
    path('std/<slug:keyword>/', views.page_std_detail, name='page_std'),
    path('series/<slug:slug>/', views.series_detail, name='series_detail'),
    path('search/', views.search, name='search'),
]


''''
Blog:
page/post/[slug]
<a href="{% url 'post_detail' post.slug %}">

page/series/[slug]
<a href="{% url 'series_detail' series.slug %}">


'''