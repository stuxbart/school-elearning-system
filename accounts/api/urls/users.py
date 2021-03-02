from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from ..views import (
    UserListAPIView,
    UserRetrieveUpdateDestroyAPIView,
    UserSearchAPIView
)

urlpatterns = [
    path('', UserListAPIView.as_view(), name="user-list"),
    path('search', UserSearchAPIView.as_view(), name="user-search"),
    path('<int:pk>', UserRetrieveUpdateDestroyAPIView.as_view(), name="user-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
