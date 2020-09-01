from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from ..views import (
    UserListAPIView,
    UserRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('', UserListAPIView.as_view(), name="user-list"),
    path('<int:pk>', UserRetrieveUpdateDestroyAPIView.as_view(), name="user-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
