from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from ..views import (
    UserListAPIView,
    UserRetrieveUpdateDestroyAPIView,
    UserSearchAPIView,
    UserNASearchAPIView
)

app_name = 'users'

urlpatterns = [
    path('', UserListAPIView.as_view(), name="user-list"),
    path('search', UserSearchAPIView.as_view(), name="user-search"),
    path('search/no-admins', UserNASearchAPIView.as_view(), name="user-search-no-admins"), # enable us to search for users that can be added to course as admins / get arg: course - id of course
    path('<int:pk>', UserRetrieveUpdateDestroyAPIView.as_view(), name="user-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
