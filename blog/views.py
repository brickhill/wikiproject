from django.shortcuts import render, get_object_or_404
from .models import Post, Page, Series
from django.db.models import Q

def post_list(request):
    posts = Post.objects.filter(status='published').order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, slug):
    print(f'post detail:{slug}')
    post = get_object_or_404(Post, slug=slug, status='published')
    return render(request, 'blog/post_detail.html', {'post': post})


def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'blog/page.html', {'page': page})


def series_detail(request, slug):
    series = get_object_or_404(Series, slug=slug)
    posts = Post.objects.filter(series=series, status='published')
    return render(request, 'blog/series.html', {'series': series, 'posts': posts})


def search(request):
    query = request.GET.get('q')

    results = Post.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query)
    )

    return render(request, 'blog/search.html', {
        'query': query,
        'results': results
    })