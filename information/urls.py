from django.urls import path

from .views import About, Statute, Contact

app_name = 'information'

urlpatterns = [
    path('about', About.as_view(), name='about'),
    path('statute', Statute.as_view(), name='statute'),
    path('contact', Contact.as_view(), name='contact'),
]