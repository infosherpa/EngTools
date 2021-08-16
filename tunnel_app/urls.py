from django.urls import path, re_path
from . import views

app_name = 'tunnel_app'
urlpatterns = [
    # ex: /tun/
    path('2', views.tunnel_app_home, name='tunnel_home'),
    path('java/', views.tunnel_app_home_w_java, name="jave_home"),
    path('', views.tunnel_app_home2, name='tunnel_home'),
    path('bugreport/', views.bugreport, name='bugreport'),

    path('frame', views.tunnel_frame_success, name='results'),
    path('java/api/form/<slug:tunnelframe_hash>/<int:form_num>', views.get_form_ajax, name="get_form_ajax"),
    path('java/api/form/post/', views.ajax_post_view, name="ajax"),
    path('<slug:tunnelframe_hash>/', views.auth_tunnel_frame_success, name='auth_results'),
    path('<slug:tunnelframe_hash>/<int:load_num>', views.tunnel_delete_load, name='delete_load'),

]


