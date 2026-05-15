from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
import resend
from django.conf import settings
# MAJOR Add contact form.
# XXX Home page text
# XXX T&C
# XXX Privacy
# XXX List of series in a sidebar.
# MAJOR Add SEO to posts and pages.
# MAJOR 'My account' to change username, password etc.

def home(request):
    # return HttpResponse("Hello, worldx!")
    context = {
        "title": "My Django Site",
        "message": "Welcome to the homepage",
    }
    return render(request, "home.html", context)


def about(request):
    context = {}
    return render(request, "about.html", context)


@login_required
def member(request):
    # TODO Add sbsys.co.uk to resend.
    context = {
        "content1": "<h1>Content11</h1>",
        "left": "stuff on the left"
    }
    # TODO Incorporate this email sending logic elsewhere.
    # resend.api_key = settings.RESEND_API_KEY

    # r = resend.Emails.send({
    #                         "from": "onboarding@resend.dev",
    #                         "to": "petergibson@sbsys.co.uk",
    #                         "subject": "Test Email",
    #                         "html": """
    #                         <p>Congrats on sending your <strong>first email</strong>!</p>
    #                         """
    #                         })

    return render(request, "member.html", context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})
