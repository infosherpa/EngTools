from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LogoutForm
from django.contrib.auth.views import LogoutView
from django.views.generic.base import TemplateView
from tunnel_app.models import TunnelFrame

# Create your views here.


def login(request):
    _message = "Please Log In"
    if request.method == 'POST':
        _password = request.POST['password']
        _username = request.POST['username']
        user = authenticate(username=_username, password=_password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                _message = "Your account is not activated"
        else:
            _message = "Invalid Login"
    context = {'message': _message}
    return render(request, 'registration/login.html', context=context)


class AccLogoutView(LogoutView):
    next_page = ""
    template_name = "registration/logout.html"


class ProfileView(TemplateView):
    template_name = "registration/profile.html"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['Frames'] = TunnelFrame.objects.filter(creator=user)
        print(context)
        return context
