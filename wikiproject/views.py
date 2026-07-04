from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, ContactForm
from blog.models import Page
from django.contrib.auth.views import LoginView, LogoutView
import resend
from django.conf import settings


class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, "You are already logged in.")
            return redirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(
            self.request,
            f"Welcome back, "
            f"{form.get_user().first_name or form.get_user().username}!"
        )
        return super().form_valid(form)


class MyLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You are already logged out.")
            return redirect("home")
        messages.success(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)


def server_error(request):
    return render(request, "500.html", status=500)


def home(request):
    page = get_object_or_404(Page, keyword='home')
    hero = get_object_or_404(Page, keyword='hero')
    context = {
        "title": page.title,
        "content": page.content,
        "hero_title": hero.title,
        "hero_content": hero.content,
        "image": page.image,
        "image_title": "TBA"
    }
    return render(request, "home.html", context)


@login_required
def member(request):
    title = "Member"
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
                f'Message sent successfully.'
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
