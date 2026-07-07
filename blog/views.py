from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Page, Series, Comment, SeriesPost, Category
from django.db.models import Q
from .forms import CommentForm
from django.contrib import messages


def post_list(request):
    posts = Post.objects.filter(status='published',
                                published_date__isnull=False).  \
                                order_by('-published_date')
    title = "Blog Posts"
    request.session["last_blog_page"] = request.get_full_path()
    request.session["last_label"] = "Back to Blog"
    return render(request, 'blog/post_list.html', {'posts': posts,
                                                   'title': title})


def post_detail(request, slug, series=None):
    back_url = request.session.get("last_blog_page")
    back_label = request.session.get("last_label")
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
                messages.success(request,
                                 'Your comment is awaiting approval')
                return redirect('post_detail', slug=slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'back_url': back_url,
        'back_label': back_label,
        'title': post.title,
        'form': form,
        'series': series,
        'content1': True
    })


def page_detail(request, slug):

    page = get_object_or_404(Page, slug=slug)
    return render(request, 'blog/page.html', {'page': page})


def page_std_detail(request, keyword):
    # messages.success(
    #             request,
    #             'SUCCESS'
    #         )
    # messages.debug(
    #     request,
    #     "What is this?"
    # )
    # messages.error(
    #                request,
    #                'Something went wrong.'
    # )
    # messages.warning(request, 'Be careful.')
    # messages.info(request, 'FYI...')
    page = get_object_or_404(Page, keyword=keyword)
    return render(request, 'blog/page.html', {'page': page})


def category_detail(request, id):
    request.session["last_blog_page"] = request.get_full_path()
    category = get_object_or_404(Category, id=id)
    request.session["last_label"] = "Back to " + category.name
    posts = category.posts.all()     # type: ignore
    context = {
        "content1": "Cat detail",
        "category": category,
        "posts": posts
    }
    return render(request, 'blog/category_detail.html', context)


def series_detail(request, id):
    print("NOB")
    request.session["last_blog_page"] = request.get_full_path()
    series = get_object_or_404(Series, id=id)
    request.session["last_label"] = f"Back to Series: {series}"
    seriesposts = SeriesPost.objects.filter(
        series=series).select_related("post").order_by("order")
    print("POSTS START")
    for p in seriesposts:
        print(f"SERIESPOST:{p.post.title}")

    print("POST END")
    context = {
        "series": series,
        "content1": "CONTENT1",
        "seriesposts": seriesposts,
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
