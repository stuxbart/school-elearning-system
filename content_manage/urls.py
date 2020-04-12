from django.urls import path, include

from .views import ManageCourseList, ManageCourseEdit

app_name = 'manage'

urlpatterns = [
    path('', ManageCourseList.as_view(), name='list'),
    path('course/', ManageCourseEdit.as_view(), name="create"),
    path('course/<slug>', ManageCourseEdit.as_view(), name="update"),
]
