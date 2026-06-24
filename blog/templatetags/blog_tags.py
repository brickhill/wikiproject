# blog/templatetags/blog_tags.py
from django import template
from django.shortcuts import get_object_or_404
from blog.models import Post, Series, SeriesPost, Category

register = template.Library()


@register.inclusion_tag('includes/recent_posts.html')
def recent_posts(count=5):
    posts = Post.objects.filter(status='published'). \
            order_by('-published_date')[:count]
    return {'recent_posts': posts}

@register.inclusion_tag('includes/categories.html')
def categories():
    categories = Category.objects.all()
    # categories = ['A', 'B', 'C', "D"]
    return {'categories': categories }

@register.inclusion_tag('includes/list_series.html')
def list_series():
    # TODO Series should have 'draft/published' flag and a priority.
    series = Series.objects.all().order_by('slug')
    return {'list_series': series}


@register.inclusion_tag('includes/blog_panel.html')
def blog_panel(post=None, series=None):
    if series is not None:
        series = get_object_or_404(Series, slug=series)
    posts = SeriesPost.objects.filter(
        series=series).select_related("post").order_by("order")

    context = {"posts": posts, "series": series, "post": post}
    '''
    post is current post.
    posts are all posts in series.
    '''
    return context

@register.inclusion_tag('includes/format_pub_author.html')
def format_pub_author(published=None, author=None):
    context = {"published": published, "author": author}
    return context
