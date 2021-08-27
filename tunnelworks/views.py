from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string


def index(request):
    """The Base index page for the entire site"""
    return render(request, 'home.html')


def about(request):
    """The Base index page for the entire site"""
    return render(request, 'about.html')


def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)


def error_500(request):
    data = {}
    return render(request, '500.html', data)




