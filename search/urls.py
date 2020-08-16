from django.urls import path

from .views import MainSearchView
app_name = 'search'

urlpatterns = [
    path('', MainSearchView.as_view(), name='main')
]