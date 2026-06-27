from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Page, Series, Comment, SeriesPost, Category
from django.db.models import Q
from .forms import CommentForm
from django.contrib import messages


def post_list(request):
    posts = Post.objects.filter(status='published').order_by('-published_date')
    title = "Blog Posts"
    return render(request, 'blog/post_list.html', {'posts': posts,
                                                   'title': title})


def post_detail(request, slug, series=None):
    # if series is None:
    #     print("NORMAL BLOG")
    post = get_object_or_404(
        Post,
        slug=slug,
        status='published'
    )
    comments = Comment.objects.filter(
        post=post,
        active=True,
        parent__isnull=True
    )
    form = CommentForm()

    if request.method == 'POST':

        if request.user.is_authenticated:

            form = CommentForm(request.POST)

            if form.is_valid():

                comment = form.save(commit=False)

                comment.post = post
                comment.user = request.user

                parent_id = request.POST.get('parent_id')

                if parent_id:
                    comment.parent = Comment.objects.get(id=parent_id)

                comment.save()

                return redirect('post_detail', slug=slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'title': post.title,
        'form': form,
        'series': series,
        'content1': True
    })


def page_detail(request, slug):

    page = get_object_or_404(Page, slug=slug)
    return render(request, 'blog/page.html', {'page': page})


def page_std_detail(request, keyword):
    messages.success(
                request,
                'SUCCESS'
            )
    messages.debug(
        request,
        "What is this?"
    )
    messages.error(
                   request,
                   'Something went wrong.'
    )
    messages.warning(request, 'Be careful.')
    messages.info(request, 'FYI...')
    page = get_object_or_404(Page, keyword=keyword)
    return render(request, 'blog/page.html', {'page': page})


def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    context = {
        "content1": "Cat detail",
        "category": category
    }
    return render(request, 'blog/category_detail.html', context)


def series_detail(request, slug):
    series = get_object_or_404(Series, slug=slug)
    posts = SeriesPost.objects.filter(
        series=series).select_related("post").order_by("order")

    context = {
        "series": series.slug,
        "content1": "CONTENT1",
        "posts": posts,
    }
    return render(request, 'blog/series_detail.html', context)


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
