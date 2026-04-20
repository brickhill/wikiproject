from django.http import HttpResponse
from django.views.generic import DetailView


def home(request):
    return HttpResponse("Hello, world!")