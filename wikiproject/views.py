from django.http import HttpResponse
from django.views.generic import DetailView
from django.shortcuts import render, redirect
from .forms import RegisterForm

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



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})