from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from knox import views as knox_views

from ..views import (
    RegisterAPIView,
    LoginAPIView
)


urlpatterns = [
    path('', include('knox.urls')),
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('logout', knox_views.LogoutView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
