from django.urls import path, include, re_path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.ProfileView.as_view(), name="profile"),
    re_path('^login/$', views.login, name="login"),
    re_path('logout/', views.AccLogoutView),
]
