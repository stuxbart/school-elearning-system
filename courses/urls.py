
from django.urls import path, include

from .views import CourseListView, CourseDetailView, enroll_course

app_name = 'courses'

urlpatterns = [
    path('', CourseListView.as_view(), name='home'),
    path('details/<slug>/', CourseDetailView.as_view(), name='details'),
    path('enroll/', enroll_course, name='enroll')
]
