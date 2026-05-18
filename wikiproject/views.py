from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ContactForm
from blog.models import Page

import resend
from django.conf import settings
# XXX List of series in a sidebar.
# MAJOR Add SEO to posts and pages.
# MAJOR 'My account' to change username, password etc.

# TODO Don't die if std page is not present.


def home(request):
    page = get_object_or_404(Page, keyword='home')
    context = {
        "title": page.title,
        "content": page.content,
        "image": page.image
    }
    return render(request, "home.html", context)


def about(request):
    context = {}
    return render(request, "about.html", context)


@login_required
def member(request):
    title = "Member"
    # TODO Add sbsys.co.uk to resend.
    context = {
        "content1": "<h1>Content11</h1>",
        "left": "stuff on the left",
        "title": title
    }

    return render(request, "member.html", context)


def contact(request):

    if request.method == 'POST':

        form = ContactForm(request.POST)

        if form.is_valid():

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            full_message = f"""
                            From: {name}
                            Subject: {subject}
                            Email: {email}

                            {message}
            """

            resend.api_key = settings.RESEND_API_KEY

            r = resend.Emails.send({
                                    "from": "onboarding@resend.dev",
                                    "to": "petergibson@sbsys.co.uk",
                                    "subject": "Contact from www.sbsys.co.uk",
                                    "html": full_message
                                    })

            messages.success(
                request,
                f'Message sent successfully:{r}.'
            )

            return redirect('contact')

    else:

        form = ContactForm()

    return render(
        request,
        'contact.html',
        {'form': form}
    )


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})
