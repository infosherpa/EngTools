from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string


def index(request):
    """The Base index page for the entire site"""
    return render(request, 'home.html')






