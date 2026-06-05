# blog/templatetags/blog_tags.py
from django import template
from blog.models import Post, Series
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Page, Series, Comment, SeriesPost

register = template.Library()

@register.inclusion_tag('includes/recent_posts.html')
def recent_posts(count=5):
    posts = Post.objects.filter(status='published').order_by('-published_date')[:count]
    return {'recent_posts': posts}

@register.inclusion_tag('includes/list_series.html')
def list_series():
    # TODO Series should have 'draft/published' flag and a priority.
    series = Series.objects.all().order_by('slug')
    return {'list_series': series}

@register.inclusion_tag('includes/blog_panel.html')
def blog_panel(post=None, series=None):
    print(f"BLOGPOST:{post}")
    series = get_object_or_404(Series, slug=series)
    posts = SeriesPost.objects.filter(
        series=series).select_related("post").order_by("order")
    for p in posts:
        print(p.post.title)
    context = {"posts": posts, "series": series, "post": post}
    '''
    post is current post.
    posts are all posts in series.
    '''
    return context 
