# blog/templatetags/blog_tags.py
from django import template
from blog.models import Post

register = template.Library()

@register.inclusion_tag('includes/recent_posts.html')
def recent_posts(count=5):
    posts = Post.objects.filter(status='published').order_by('-published_date')[:count]
    return {'recent_posts': posts}