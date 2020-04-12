from django.urls import path, include

from .views import ManageCourseList

app_name = 'manage'

urlpatterns = [
    path('', ManageCourseList.as_view(), name='list'),
]
