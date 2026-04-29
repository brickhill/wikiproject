from django.http import HttpResponse
from django.views.generic import DetailView
from django.shortcuts import render



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