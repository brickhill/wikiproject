from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
import resend
from django.conf import settings


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
    context = {}
    resend.api_key = settings.RESEND_API_KEY

    r = resend.Emails.send({
                            "from": "onboarding@resend.dev",
                            "to": "petergibson@sbsys.co.uk",
                            "subject": "Test Email",
                            "html": """
                            <p>Congrats on sending your <strong>first email</strong>!</p>
                            """
                            })

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
