from django.shortcuts import render
from django.views.generic import TemplateView


class About(TemplateView):
    template_name = 'information/about.html'


class Statute(TemplateView):
    template_name = 'information/statute.html'


class Contact(TemplateView):
    template_name = 'information/contact.html'
