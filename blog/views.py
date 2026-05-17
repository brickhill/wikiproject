from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Page, Series, Comment
from django.db.models import Q
from .forms import CommentForm
from django.contrib import messages
# TODO 'Back to posts button on blog detail could be replicated elsewhere.
# TODO Does going back to blog list preserve page number?

def post_list(request):
    posts = Post.objects.filter(status='published').order_by('-published_date')
    title = "Blog Posts"
    return render(request, 'blog/post_list.html', {'posts': posts,
                                                   'title': title})

# TODO What to do if no Categories defined?


def post_detail(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        status='published'
    )

    comments = post.comments.filter(
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
        'form': form
    })
# TODO Spruce up blog detail page.
# TODO Only show approved commments.
# TODO Add comment rate limiting.
# TODO Add comment CAPTCHCA
# TODO Add comment Akismet
# TODO Add Ajax comments.
# TODO Add comment upvotes/downvotes
# TODO Add comment notifications.
# TODO Add comment mentions.
# TODO Add avator to user.


def page_detail(request, slug):

    page = get_object_or_404(Page, slug=slug)
    return render(request, 'blog/page.html', {'page': page})


def page_std_detail(request, keyword):
    # TODO Blog page on flash messages.
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


def series_detail(request, slug):
    series = get_object_or_404(Series, slug=slug)
    posts = Post.objects.filter(series=series, status='published')
    return render(request, 'blog/series.html',
                  {'series': series, 'posts': posts})


def search(request):
    query = request.GET.get('q')

    results = Post.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query)
    )
# TODO Search results isn't styled.
    return render(request, 'blog/search.html', {
        'query': query,
        'results': results
    })
