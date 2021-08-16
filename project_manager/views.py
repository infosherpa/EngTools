from django.shortcuts import render
from django.views.generic.base import TemplateView, View, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin


class ProjectManagementView(LoginRequiredMixin, TemplateView):

    template_name = "project_control_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        pass


class ProjectDetailView(LoginRequiredMixin, TemplateView):

    template_name = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        pass
