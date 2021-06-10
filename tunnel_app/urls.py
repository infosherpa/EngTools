from django.urls import path
from . import views

app_name = 'tunnel_app'
urlpatterns = [
    path('', views.tunnel_home, name='tunnel_home'),
    path('process/', views.tunnel_frame_input_form, name='dim_form')
]
