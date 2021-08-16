from django.urls import path, re_path
from . import views

urlpatterns = [
    path('<username>/projects', views.ProjectManagementView, name='project-home'),
    path('<username>/projects/<int:projectID>', views.ProjectDetailView, name='project-detail')
]