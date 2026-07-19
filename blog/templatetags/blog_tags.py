# blog/templatetags/blog_tags.py
from django import template
from django.db.models import Count
from django.shortcuts import get_object_or_404
from blog.models import Post, Series, SeriesPost, Category
from blog.forms import SearchForm

register = template.Library()

@register.inclusion_tag('includes/search.html')
def searchbox():
    form = SearchForm()
    return {'search_form': "SEARCH FORM", 'form': form }

@register.inclusion_tag('includes/recent_posts.html')
def recent_posts(count=5):
    posts = Post.objects.filter(status='published'). \
            order_by('-published_date')[:count]
    return {'recent_posts': posts}

@register.inclusion_tag('includes/categories.html')
def categories():

    categories = Category.objects.filter(parent__isnull=True)
    return {'categories': categories }

@register.inclusion_tag('includes/list_series.html')
def list_series():

    series = Series.objects.filter(status="published").  \
        order_by('priority').annotate(post_count=Count("seriespost"))
    return {'list_series': series}


@register.inclusion_tag('includes/blog_panel.html')
def blog_panel(post=None, series=None, category=None):
    posts = None
    if series is not None:
        series = get_object_or_404(Series, slug=series)
        posts = SeriesPost.objects.filter(
            series=series, post__status="published").select_related("post").order_by("order")
    elif category is not None:
        posts = Post.objects.filter(
            categories=category, status="published").order_by('-published_date'
        )
    context = {"posts": posts, "series": series, "post": post, "category": category}
    '''
    post is current post.
    posts are all posts in series.
    '''
    return context

@register.inclusion_tag('includes/format_pub_author.html')
def format_pub_author(published=None, author=None):
    context = {"published": published, "author": author}
    return context
