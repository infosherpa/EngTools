from django.urls import path
from . import views

app_name = 'tunnel_app'
urlpatterns = [
    # ex: /tun/
    path('', views.tunnel_app_home, name='tunnel_home'),
    #
    path('frame', views.tunnel_frame_success, name='results'),
    path('<int:tunnelframe_id>/frame/', views.auth_tunnel_frame_success, name='auth_results'),
]


