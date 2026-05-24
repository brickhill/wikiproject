# blog/templatetags/blog_tags.py
from django import template
from blog.models import Post, Series

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
