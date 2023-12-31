import datetime
#
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.urls import reverse_lazy, reverse

from django.views.generic import (
    TemplateView
)

class FechaMixin(object):

    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        context['fecha'] = datetime.datetime.now()
        return context
    

class HomePage(LoginRequiredMixin, FechaMixin, TemplateView):
    template_name = "home/index.html"

    #que sucede cuando el usuario quiere ingresar y no esta logeado. Este atributo es necesario para LoginRequiredMixin
    login_url = reverse_lazy('users_app:user-login')


class TemplatePruebaMixin(FechaMixin, TemplateView):
    template_name = "home/mixin.html"
